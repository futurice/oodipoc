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
import eyes
from sqlite3 import Error
from collections import deque

import mir_calls
import travel
import idle
import advise
import feedback
import sierra
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def find_books_from_local_database(searchtext):
    database = "mir.db"
    # create a database connection
    conn = create_connection(database)
    conn.row_factory = dict_factory

    searchtext = searchtext.lower()

    print("debug: there is a database connection")

    cur = conn.cursor()

    cur.execute("SELECT DISTINCT title, author FROM books WHERE lower(title) LIKE ?", ('%'+searchtext+'%',))

    rows = cur.fetchall()
    return rows

def find_side_by_category(category, type):
    database = "mir.db"
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
        return "l"

    return "r"

def check_for_new_mission():
    database = "mir.db"
    conn = create_connection(database)
    cur = conn.cursor()
 
    cur.execute("SELECT callnumber FROM missions WHERE status = 'new'") 
    rows = cur.fetchall()

    for row in rows:
      return row[0]

def change_mission_status():
    database = "mir.db"
    conn = create_connection(database)
    cur = conn.cursor()

    sql = "UPDATE missions SET status = 'old' WHERE status = 'new'"
    cur.execute(sql)
    conn.commit()

def find_position_by_category(category, type):
    database = "mir.db"
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

def switch_flask_view(view):
    f = open("/home/furhatdemo/OodiUI/OodiUI/static/direction.txt", "w+")
    f.write(view)
    f.close()

def main():

    #set counter to 0
    counter = 0

    # is this a category-only mission
    catmission = False

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


                if catmission == True:

                    print("DEBUG: catmission true, cat " + category);

                    if category == '79000':
                       switch_flask_view('r')                        

                    if category == '46900':
                       switch_flask_view('r')                        

                    if category == '69110':
                       switch_flask_view('lr')                        

                    if category == '85000':
                       switch_flask_view('r')                        

                    if category == '99000':
                       switch_flask_view('l')                        

                    if category == '90000':
                       switch_flask_view('l')                        

                    time.sleep(10)
                    mir_calls.add_to_mission_queue("beb5b742-341b-11e9-a33f-94c691a3a93e")
                    robot_status = 'homing'
                    time.sleep(2)
                    #eyes.lookDown()
                    catmission = False
                    sierra.update_target_time()
                    continue

                # FLASK: display arrow to left or right
                side = find_side_by_category(category, "column")
                switch_flask_view(side)
                print("debug: the book could be on the " + side + " side")

               # if side == 'r':
                    #eyes.lookLeft()

                #if side == 'l':
                    #eyes.lookRight()

                time.sleep(5)

                # the category should be mapped to a physical oodi position recognised by the mir robot
                print("debug: move to the correct column")
                positionguid = str(find_position_by_category(category, "column"))
                print("debug: position guid for category column from database is " + positionguid)
                # if we have a position, we can create a mission
                mir_calls.modify_mir_mission(positionguid)
                # add the modified travel mission to the queue
                mir_calls.add_to_mission_queue("2e066786-3424-11e9-954b-94c691a3a93e")

                # set the robot status to be on a mission
                robot_status = 'columnmission'
                switch_flask_view("blank")
              
                # give the MiR a few seconds to react so we enter the correct state (mission executing)
                time.sleep(2)

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
                switch_flask_view(side)
                sierra.update_target_time()

                print("debug: the book could be on the " + side + " side")
                time.sleep(10)
                #switch_flask_view("blank")

                # move forward one meter to make room for the customer
                #mir_calls.add_to_mission_queue("3ac4fc26-3f3f-11e9-9822-94c691a3a93e")
                #time.sleep(10) 

                # TODO ask for feedback! maybe not?
                mir_calls.add_to_mission_queue("beb5b742-341b-11e9-a33f-94c691a3a93e")
                robot_status = 'homing'
                #eyes.lookDown()
                time.sleep(5)
            
            time.sleep(1)
            continue

        if robot_status == 'homing':
            mir_status = travel.move()
            print("debug: homing in progress, mir state: " + mir_status)

            switch_flask_view("home")

            if mir_status == 'Ready': 
                print("debug: homing has been accomplished")
                print("debug: enter idle loop")
                switch_flask_view("home2")
                robot_status = 'idle'
                #eyes.lookLeft()
                #eyes.lookRight()
                #eyes.lookDown()
                sierra.update_home_time()

            time.sleep(1)
            continue

        print("debug: checking if we have a new mission")

        ### NEW MISSION AVAILABLE? if there's a category entry in missions table with status new, we have a new mission

        category = check_for_new_mission()

        if category is not None:

            # a quick hack to allow for the category missions
            if category == '79000':
                positionguid = 'aac480fd-44d5-11e9-b653-94c691a3a93e'
                catmission = True

            if category == '46900':
                positionguid = '48e76bd3-44d4-11e9-b653-94c691a3a93e'
                catmission = True

            if category == '69110':
                positionguid = '78795881-44d5-11e9-b653-94c691a3a93e'
                catmission = True

            if category == '85000':
                positionguid = 'b955c6f0-4bb0-11e9-98e7-94c691a3a93e'
                catmission = True

            if category == '99000':
                positionguid = 'd8585103-4bb0-11e9-98e7-94c691a3a93e'
                catmission = True

            if category == '90000':
                positionguid = 'eb62e8a2-4bb0-11e9-98e7-94c691a3a93e'
                catmission = True

            if catmission == True:
                print("DEBUG: catmission is true!")
                change_mission_status()

            # the category should be mapped to a physical oodi position recognised by the mir robot
            if catmission == False:
                print("debug: received target category is " + category)
                change_mission_status()
                positionguid = str(find_position_by_category(category, "shelf"))
                print("debug: position guid for category shelf from database is " + positionguid)

            # if we have a position, we can create a mission
            mir_calls.modify_mir_mission(positionguid)

            # finally add the modified shelf/column mission to the queue
            mir_calls.add_to_mission_queue("2e066786-3424-11e9-954b-94c691a3a93e")

            # set the robot status to be on a mission
            robot_status = 'shelfmission'

            # give the MiR a few seconds to react so we enter the correct state (mission executing)
            time.sleep(3)

            # eye movement :D
            #eyes.topRoll()

            continue

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
        mir_calls.add_to_mission_queue("beb5b742-341b-11e9-a33f-94c691a3a93e")
        robot_status = 'homing'
        time.sleep(2)
        continue

if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()
