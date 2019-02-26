#!/usr/bin/env python

"""
A module for controlling a MiR 200 robot at Oodi
https://github.com/futurice/oodipoc
"""

from __future__ import print_function

import sys
import subprocess

def get_mir_auth():
    # read the basic auth token off a file outside this repository
    mir_auth = open("../.mir_auth").readline()
    # readline adds a newline to the end, so strip that
    mir_auth = mir_auth.rstrip('\n')
    return mir_auth

def get_mir_status():
    # get the current status from the mir robot 
    command = 'curl -sb GET "http://mir.com/api/v2.0.0/status" -H "accept: application/json" -H "' + get_mir_auth() + '" -H "Accept-Language: en_US" | egrep "state_text" | tr -d " " | cut -d\'"\' -f4'
    print(command)
    #state = subprocess.run(command)
    #print("State: " + state)

def delete_mir_move_action():
    # delete a certain action from our move-to-location mir mission via curl call to rest api
    command = 'curl -sb DELETE "http://mir.com/api/v2.0.0/missions/2e066786-3424-11e9-954b-94c691a3a93e/actions/11111111-1111-1111-1111-111111111111" -H "accept: application/json" -H "' + get_mir_auth() + '" -H "Accept-Language: en_US"'
    print(command)

def add_mir_move_action(position):
    # add a move action to a defined location into our move-to-location mir mission via curl call to rest api
    # placeholder until the position guid mapping logic is there 
    position = "0b676baa-3423-11e9-954b-94c691a3a93e"

    command = 'curl -sb POST "http://mir.com/api/v2.0.0/missions/2e066786-3424-11e9-954b-94c691a3a93e/actions" -H "accept: application/json" -H "' + get_mir_auth() + '" -H "Accept-Language: en_US" -H "Content-Type: application/json" -d "{ \"action_type\": \"move\", \"mission_id\": \"2e066786-3424-11e9-954b-94c691a3a93e\", \"guid\": \"11111111-1111-1111-1111-111111111111\", \"parameters\": [ { \"guid\": \"2e9e391a-3424-11e9-954b-94c691a3a93e\", \"id\": \"position\", \"input_name\": null, \"value\": \"' + position + '\" }, { \"guid\": \"2ea2b83c-3424-11e9-954b-94c691a3a93e\", \"id\": \"retries\", \"input_name\": null, \"value\": 1 }, { \"guid\": \"2ea788d7-3424-11e9-954b-94c691a3a93e\", \"id\": \"distance_threshold\", \"input_name\": null, \"value\": 0.1 } ], \"priority\": 1, \"url\": \"/v2.0.0/mission_actions/2e9758a2-3424-11e9-954b-94c691a3a93e\" }"'
    print(command)

def modify_mir_mission(position):
    # todo make use of the mir mission modifying calls to setup our move-to-location mir mission to match the book/category location
    delete_mir_move_action()
    add_mir_move_action(position)
    get_mir_status()
