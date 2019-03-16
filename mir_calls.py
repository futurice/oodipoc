#!/usr/bin/env python

"""
A module for controlling a MiR 200 robot at Oodi
https://github.com/futurice/oodipoc
"""

from __future__ import print_function

import sys
import subprocess
import json
import requests

def get_mir_auth():
    # read the basic auth token off a file outside this repository
    mir_auth = open("../.mir_auth").readline()
    # readline adds a newline to the end, so strip that
    mir_auth = mir_auth.rstrip('\n')
    return mir_auth

def get_headers():
    auth = get_mir_auth()
    headers = {'accept': 'application/json', 'Authorization': auth, 'Accept-Language': 'en_US', 'Content-Type': 'application/json'}
    return headers

def add_to_mission_queue(mission = "beb5b742-341b-11e9-a33f-94c691a3a93e"):
    
    # add a mission to the mission queue (default is return to homebase)

    # 3ac4fc26-3f3f-11e9-9822-94c691a3a93e is relative X move 1 meter

    url = 'http://mir.com/api/v2.0.0/mission_queue'
    headers = get_headers()

    data = {
    "mission_id": mission,
    "priority": 0
    }
    
    response = requests.post(url, headers=headers, json=data)

def get_mir_status():

    # get the current status from the mir robot 

    url = 'http://mir.com/api/v2.0.0/status'
    headers = get_headers()

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    try:
    	return json_data["state_text"]
    except KeyError as error:
        print("debug: got KeyError trying to read MiR status")
        print(json_data)
        return "status-fetch-error"

def delete_mir_move_action():

    # delete a certain action from our move-to-location mir mission via curl call to rest api

    print("debug: delete mir move action called")

    url = 'http://mir.com/api/v2.0.0/missions/2e066786-3424-11e9-954b-94c691a3a93e/actions/11111111-1111-1111-1111-111111111111'
    headers = get_headers()
    response = requests.delete(url, headers=headers)

def delete_mir_reaction_sound_action():

    # delete a certain action from our move-to-location mir mission via curl call to rest api

    url = 'http://mir.com/api/v2.0.0/missions/d6184d0f-3a94-11e9-b2d2-94c691a3a93e/actions/11111111-1111-1111-1111-111111111112'
    headers = get_headers()
    response = requests.delete(url, headers=headers)

def add_mir_move_action(positionguid = "0b676baa-3423-11e9-954b-94c691a3a93e"):

    # add a move action to a defined location into our move-to-location mir mission via curl call to rest api

    print("debug: add mir move action called")

    url = "http://mir.com/api/v2.0.0/missions/2e066786-3424-11e9-954b-94c691a3a93e/actions"
    headers = get_headers()

    data = {
    "action_type": "move", 
    "guid": "11111111-1111-1111-1111-111111111111", 
    "mission_id": "2e066786-3424-11e9-954b-94c691a3a93e", 
    "parameters": [ 
      { 
        "id": "position", 
        "value": positionguid
      }, 
      { 
        "id": "retries", 
        "value": 10 
      }, 
      { 
         "id": "distance_threshold", 
         "value": 0.1 
      } 
    ], 

    "priority": 1, 
    "url": "/v2.0.0/mission_actions/2e9758a2-3424-11e9-954b-94c691a3a93e"
    }

    response = requests.post(url, headers=headers, json=data)

def add_mir_reaction_sound(sound = "45f02254-d6a5-11e8-8995-94c691a3e21e", priority = 1, volume = 100):

   # prioriy = which action within the mission
   # volume = 1-100
   # woops = 45f02254-d6a5-11e8-8995-94c691a3e21e
   # ticketytick = 6ee40f76-3aac-11e9-800b-94c691a3a93e

    url = "http://mir.com/api/v2.0.0/missions/d6184d0f-3a94-11e9-b2d2-94c691a3a93e/actions"
    headers = get_headers()

    data = {
    "action_type": "sound",
    "guid": "11111111-1111-1111-1111-111111111112",
    "mission_id": "d6184d0f-3a94-11e9-b2d2-94c691a3a93e",
    "parameters": [
      {
        "id": "sound",
        "value": sound
      },
      {
        "id": "volume",
        "value": volume
      },
      {
        "id": "mode",
        "value": "full"
      },
      {
        "id": "duration",
        "value": "00:00:01.000000"
      }
    ],

    "priority": priority,
    "url": "/v2.0.0/mission_actions/d6184d0f-3a94-11e9-b2d2-94c691a3a93e"
    }

    response = requests.post(url, headers=headers, json=data)

def modify_mir_mission(position):

    # todo make use of the mir mission modifying calls to setup our move-to-location mir mission to match the book/category location

    delete_mir_move_action()
    add_mir_move_action(position)
    #get_mir_status()
