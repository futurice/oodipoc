#!/usr/bin/env python

"""
A script for controlling a MiR 200 robot at Oodi, developed with python3, sqlite3, on osx
https://github.com/futurice/oodipoc
"""

from __future__ import print_function

import os
import sys
import time
import subprocess
import sqlite3
from sqlite3 import Error
from collections import deque

import mir_calls
import travel
import idle
import advise
import feedback
from emotions import Emotion

#global variables counter (counts how many loops have executed), statushistory (places last 50 statuses in stack), emotions (robots emotion state)
global counter
global statushistory
global emotions


def syntax(execname):
    print("Syntax: %s" % execname)
    sys.exit(1)

def create_connection(db_file):
    """ create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def find_side_by_category(category, type):
    database = "/Users/ttur/Documents/oodipoc/mir.db"
    # create a database connection
    conn = create_connection(database)

    print("debug: there is a database connection")

    cur = conn.cursor()

    if type == "shelf": 
        cur.execute('''SELECT guid FROM shelfpositions WHERE minCategoryLeft <= ? AND maxCategoryLeft >= ?''', (category,category))
    elif type == "column":
        cur.execute('''SELECT guid FROM columnpositions WHERE minCategoryLeft <= ? AND maxCategoryLeft >= ?''', (category,category))

    rows = cur.fetchall()

    if len(rows) > 0:
        return "left"

    return "right"

def find_position_by_category(category, type):
    database = "/Users/ttur/Documents/oodipoc/mir.db"
    # create a database connection
    conn = create_connection(database)

    print("debug: there is a database connection")

    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()

    if type == "shelf": 
        cur.execute('''SELECT guid FROM shelfpositions WHERE (minCategoryLeft <= ? AND maxCategoryLeft >= ?) OR (minCategoryRight <= ? AND maxCategoryRight >= ?)''', (category,category,category,category))
        print("debug: SQL select has been executed to find the shelf position guid")
    elif type == "column":
        cur.execute('''SELECT guid FROM columnpositions WHERE (minCategoryLeft <= ? AND maxCategoryLeft >= ?) OR (minCategoryRight <= ? AND maxCategoryRight >= ?)''', (category,category,category,category))
        print("debug: SQL select has been executed to find the column position guid")

    rows = cur.fetchall()

    for row in rows:
      return row[0]

def main():

    #set counter to 0
    counter = 0

    #create stack for status histories
    statushistory = deque([],50)

    #create emotion table
    emotions = Emotion(9)
    emotions.create_area("angry", 0, 0, 2, 2)
    emotions.create_area("frustrated", 0, 3, 2, 5)
    emotions.create_area("sad", 0, 6, 2, 8)
    emotions.create_area("bored", 3, 0, 5, 8)
    emotions.create_area("excited", 6, 0, 8, 2)
    emotions.create_area("happy", 6, 3, 8 ,5)
    emotions.create_area("ok", 6, 6, 8, 8)

    # primary status, possibilities are: idle = waiting for customers, mission = on a mission, advising = telling where the book is, feedback = waiting for or reacting to feedback
    robot_status = "feedback"

    print("ROBOT STATUS: " + robot_status)

    while True:
        #get robot status
        status = mir_calls.get_mir_status()

        if (counter%1==0):
            statushistory.append(status)

        counter = counter + 1

        print("debug: checking if we are on a mission")

        ### ON A MISSION? if yes, call the related logic in travel.py, and skip cycle

        if robot_status == 'shelfmission':
            mir_status = travel.move()
            print("debug: shelf mission in progress, mir state: " + mir_status)

            if mir_status == 'Ready':
                print("debug: shelf-mission has been accomplished")
  
                print("debug: wait for 5 seconds")
                # FLASK: display arrow to left or right
                side = find_side_by_category(category, "column")
                print("debug: the book could be on the " + side + " side")
                time.sleep(5)

                print("debug: move to the correct column")
                positionguid = str(find_position_by_category(category, "column"))
                print("debug: position guid for category column from database is " + positionguid)

                # if we have a position, we can create a mission
                mir_calls.modify_mir_mission(positionguid)
                # add the modified travel mission to the queue
                mir_calls.add_to_mission_queue("2e066786-3424-11e9-954b-94c691a3a93e")

                # set the robot status to be on a mission
                robot_status = 'columnmission'
              
                # give the MiR a few seconds to react so we enter the correct state (mission executing)
                time.sleep(3)

            time.sleep(1)
            continue

        if robot_status == 'columnmission':
            mir_status = travel.move()
            print("debug: column mission in progress, mir state: " + mir_status)

            if mir_status == 'Ready':
                print("debug: column-mission has been accomplished")
                print("debug: wait for 5 seconds")
                # FLASK: display arrow to left or right
                side = find_side_by_category(category, "column")
                print("debug: the book could be on the " + side + " side")
                time.sleep(5)

                # TODO: move one meter (?) forward 

                robot_status = 'idle'

            time.sleep(1)
            continue

        print("debug: checking if we have a new mission")

        ### NEW MISSION AVAILABLE? if there's a category.txt file, we have a new mission (placeholder implementation)

        try:
            f = open("category.txt", "r")
            category = f.readline()
            category = category.rstrip('\n')

            # the category should be mapped to a physical oodi position recognised by the mir robot
            print("debug: received target category is " + category)
            positionguid = str(find_position_by_category(category, "shelf"))
            print("debug: position guid for category shelf from database is " + positionguid)

            # if we have a position, we can create a mission
            mir_calls.modify_mir_mission(positionguid)
            # add the modified travel mission to the queue
            mir_calls.add_to_mission_queue("2e066786-3424-11e9-954b-94c691a3a93e")

            # set the robot status to be on a mission
            robot_status = 'shelfmission'

            # delete the category.txt file
            os.remove("category.txt")

            # give the MiR a few seconds to react so we enter the correct state (mission executing)
            time.sleep(3)

            continue

        except IOError:
            print("debug: checking if we are idle")

        ### NO MISSIONS? let's call the related logic in idle.py to attract customers

        if robot_status == 'idle':
          idle.idle(statushistory,emotions)
          time.sleep(1)
          continue

        if robot_status == "advising":
            advise.advise(emotions, "atColumn", "right")
            time.sleep(1)
            continue

        if robot_status == "feedback":
            feedback.feedback(emotions, 1, "good")

        ### NO STATUS, NO NEW MISSION? let's send the robot back to the homebase

        print("debug: no status, return to home")
        time.sleep(1)
        continue

if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()
