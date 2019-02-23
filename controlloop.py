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

    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT position FROM positions WHERE category=?", (category,))

    rows = cur.fetchall()
        
    for row in rows:
        return row[0]

def get_mir_auth():
    # read the basic auth token off a file outside this repository
    mir_auth = open("../.mir_auth").readline()
    # readline adds a newline to the end, so strip that
    mir_auth = mir_auth.rstrip('\n')
    return mir_auth

def get_mir_status():
    
    command = 'curl -sb GET "http://mir.com/api/v2.0.0/status" -H "accept: application/json" -H "' + get_mir_auth() + '" -H "Accept-Language: en_US" | egrep "state_text" | tr -d " " | cut -d\'"\' -f4'
    print(command)
#   state = subprocess.run(command)
#   print("State: " + state)

def get_mir_mission_details():
    # todo, get details for our move-to-location mir mission via curl call to rest api
    print("get_mir_mission_details called")

def delete_mir_action(guid):
    # todo, delete a certain action from our move-to-location mir mission via curl call to rest api
    print("delete_mir_action called with guid: " + guid)

def add_mir_action(location):
    # todo, add a move action to a defined location into our move-to-location mir mission via curl call to rest api
    print("add_mir_action called with location: " + location)

def modify_mir_mission(location):
    # todo make use of the mir mission modifying calls to setup our move-to-location mir mission to match the book/category location
    print("modify mission called with location: " + location)
    get_mir_mission_details()
    delete_mir_action("1")
    add_mir_action(location)

def main():

    while True:
        # wait for a mission

        try:
            # if there's a category.txt we have a mission
            f = open("category.txt", "r")
            category = f.readline()
            # the category should be mapped to a physical oodi position recognised by the mir robot
            position = str(find_position_by_category(category))
            # if we have a position, we can create a mission
            modify_mir_mission(position)
            # once we have a mission we can run it

            # TODO: a mission loop that checks mir status and acts accordingly 

        except IOError:
            print("Waiting for a mission ...", file=sys.stderr)

        # check every second whether we're on a mission
        time.sleep(1)
        subprocess.run("clear") 

if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()
