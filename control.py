#!/usr/bin/env python

"""
A script for controlling a MiR 200 robot at Oodi, developed with python3, sqlite3, on osx
https://github.com/futurice/oodipoc
"""

from __future__ import print_function

import sys
import time
import subprocess
import sqlite3
from sqlite3 import Error

import mir_calls
import move

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

def find_position_by_category(category):
    database = "/Users/ttur/Documents/oodipoc/mir.db"
    # create a database connection
    conn = create_connection(database)

    print("we have connection")

    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cat = category
    cur.execute('''SELECT position FROM positions WHERE category = ?''', (cat,))

    print("we have executed the select")

    rows = cur.fetchall()

    print(rows)
    print("we have fetched rows")

    for row in rows:
      return row[0]

def main():

    # primary status, possibilities are: idle = waiting for customers, mission = on a mission
    robot_status = "idle"

    print("ROBOT STATUS: " + robot_status)

    while True:

        print("checking if on a mission")

        # ON A MISSION? if yes, call the related logic in move.py, and skip cycle
        if robot_status == 'mission':
          move.move()
          time.sleep(1)           
          continue

        print("checking new mission")

        # NEW MISSION AVAILABLE? if there's a category.txt file, we have a new mission (placeholder implementation)
        try:
            f = open("category.txt", "r")
            category = f.readline()
            category = category.rstrip('\n')

            # the category should be mapped to a physical oodi position recognised by the mir robot
            print("category is " + category)
            position = str(find_position_by_category(category))
            print("position is " + position)

            # if we have a position, we can create a mission
            mir_calls.modify_mir_mission(position)
            # add the modified move mission to the queue
            mir_calls.add_to_mission_queue("2e066786-3424-11e9-954b-94c691a3a93e")

            # set the robot status to be on a mission
            robot_status = 'mission'

            continue

        except IOError:
            print("checking idle")

        # NO MISSIONS? let's call the related logic in idle.py to attract customers
        if robot_status == 'idle':
          print("attracting customers")
          time.sleep(1)
          continue

        # NO STATUS, NO NEW MISSION? let's send the robot back to the homebase
        print("no status, back to home")
        time.sleep(1)
        continue

if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()
