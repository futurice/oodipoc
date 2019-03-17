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

def get_oodi_shelved_books(textsearch):

    token = get_sierra_auth_token()
    url = 'https://kirjtuo1.helmet.fi/iii/sierra-api/v5/bibs/query?offset=0&limit=10'
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

    for element in json_data:
        for value in json_data['entries']:
                         
            if (value['location']['name'] == 'Oodi' or value['location']['name'] == 'Oodi aik'):
                code = value['status']['code']
                display = value['status']['display']

                if (code == '-' and display == 'ON SHELF'):
                    try: 
                        duedate = value['status']['duedate']
                    except KeyError:
                        return "yes"

    return "no"

def get_volume_details(bipurl):
    token = get_sierra_auth_token()
    url = bipurl
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    return json_data
