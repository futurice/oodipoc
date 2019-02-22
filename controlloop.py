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

__author__ = "Teemu Turunen"
__license__ = "MIT"

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

def get_mir_status():
    # doesn't work yet 

def main():

    while True:
        # wait for a mission

        try:
            f = open("category.txt", "r")
            category = f.readline()
            position = str(find_position_by_category(category))
            print("Position for category " + category + " is " + position) 
                        # TODO: create a mission with a move to this position and back to homebase (and other actions)
                        # TODO: requires a mission template and some testing and calls to the REST API
#           get_mir_status()

        except IOError:
            print("Waiting for a mission ...", file=sys.stderr)

        time.sleep(1)
        subprocess.run("clear") 

if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()
