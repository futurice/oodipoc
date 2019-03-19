#!/usr/bin/env python

"""
A module for integrating to the library system to fetch information on which books are available at Oodi
https://github.com/futurice/oodipoc
"""

from __future__ import print_function

import sys
import subprocess
import json
import requests
import re
import datetime
import sqlite3
from sqlite3 import Error

def get_sierra_basic_auth():
    # read the basic auth token off a file outside this repository
    sierra_auth = open("../.sierra_auth").readline()
    # readline adds a newline to the end, so strip that
    sierra_auth = sierra_auth.rstrip('\n')
    return sierra_auth

def get_sierra_auth_token():
    auth = get_sierra_basic_auth()
    url = 'https://kirjtuo1.helmet.fi/iii/sierra-api/token'
    headers = {'Authorization': auth, 'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, headers=headers)
    json_data = json.loads(response.text)
    return 'Bearer ' + json_data['access_token']

def search_shelved_books(searchtext):
    print(datetime.datetime.now())
    database = "mir.db"
    # create a database connection
    conn = create_connection(database)
    conn.row_factory = dict_factory

    searchtext = searchtext.lower()

    print("debug: there is a database connection")

    cur = conn.cursor()

    cur.execute("SELECT DISTINCT title, author, bibid FROM books WHERE (lower(title) LIKE ? OR lower(author) LIKE ?) LIMIT 20", ('%'+searchtext+'%','%'+searchtext+'%',))

    rows = cur.fetchall()

    counter = 0
    retdict = {}

    for value in rows:
        bibid = value['bibid']

        if is_book_on_shelf_in_oodi(bibid) == 'yes':
            title = value['title']
            author = value['author']

            if counter < 1:
                retdict = { bibid : {'title' : title, 'author' : author } }
                counter = counter + 1
            else:
                retdict[bibid] = {'title' : title, 'author' : author }

    print(datetime.datetime.now())
    return retdict

def get_oodi_shelved_books(textsearch):

    token = get_sierra_auth_token()
    url = 'https://kirjtuo1.helmet.fi/iii/sierra-api/v5/bibs/query?offset=0&limit=20'
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    data = {
    "queries": [
        {
            "target": {
                "record": { "type": "bib" },
                "field": { "tag": "t" }
            },
            "expr": {
                "op": "has", "operands": [ textsearch ]
            }
        },
        "and",
        {
            "target": {
                "record": { "type": "item" }, "id": 79 
            },
            "expr": {
                "op": "has", "operands": [ "h00" ]
            }
        },
        "and",
        {
            "target": {
                "record": { "type": "item" }, "id": 88
            },
            "expr": [
                { "op": "equals", "operands": [ "-" ] },
                "or",
                { "op": "equals", "operands": "o" }
            ]
        }
    ]
    }

    response = requests.post(url, headers=headers, json=data)
    json_data = json.loads(response.text)
    return json_data

def get_book_details(bipurl):
    token = get_sierra_auth_token()
    url = bipurl
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    return json_data

def is_book_on_shelf_in_oodi(bibId):
    json_data = get_book_details("https://kirjtuo1.helmet.fi/iii/sierra-api/v5/items?bibIds=" + bibId)
    callnumbers = get_included_callnumbers()

    for element in json_data:
        for value in json_data['entries']:
            if (value['location']['name'] == 'Oodi' or value['location']['name'] == 'Oodi aik'):
                code = value['status']['code']
                display = value['status']['display']
                callnumber = value['callNumber']

                if (code == '-' and display == 'ON SHELF' and callnumber in callnumbers):
                    try: 
                        duedate = value['status']['duedate']
                    except KeyError:
                        return "yes"

    return "no"

def get_book_callnumber(bibId):
    json_data = get_book_details("https://kirjtuo1.helmet.fi/iii/sierra-api/v5/items?bibIds=" + bibId)

    for element in json_data:
        for value in json_data['entries']:
            if (value['location']['name'] == 'Oodi' or value['location']['name'] == 'Oodi aik'):
                callnumber = value['callNumber']

    return callnumber

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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

def get_included_callnumbers():
    database = "mir.db"
    # create a database connection
    conn = create_connection(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT callNumber FROM books")

    rows = cur.fetchall()

    results = []
  
    for row in rows:
       results.append(row['callnumber'])

    return results

def search_shelved_books_from_sierra(searchtext):
    json_data = get_oodi_shelved_books(searchtext) 
    counter = 0
    retdict = {}

    for value in json_data['entries']:
        bipurl = value['link']
        bipid = bipurl[50:]

        if is_book_on_shelf_in_oodi(bipid) == 'yes':
            details = get_book_details(bipurl)
            title = details['title']
            author = details['author']

            if counter < 1:
                retdict = { bipid : {'title' : title, 'author' : author } }
                counter = counter + 1
            else:
                retdict[bipid] = {'title' : title, 'author' : author }

    return retdict

def get_volume_details(bipurl):
    token = get_sierra_auth_token()
    url = bipurl
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    return json_data

def add_new_book_mission(bibId):
    callnumber = get_book_callnumber(bibId)
    insert_into_mission_table(callnumber)

def insert_into_mission_table(callnumber):
    database = "mir.db"
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()

    stripalpha  = re.compile(r'[^\d.]+')
    cnumber = stripalpha.sub('', callnumber)
    status = 'new'

    sql = "INSERT INTO missions (callnumber, status) VALUES (?, ?)"
    cur.execute(sql, (cnumber, status))
    conn.commit()
