#!/usr/bin/env python

"""
A module for monitoring MiR 200 robot mission status and acting accordingly
Called by the control.py controller module
https://github.com/futurice/oodipoc
"""

from __future__ import print_function

import sys
import time
import subprocess

import mir_calls
import emotions


def syntax(execname):
    print("Syntax: %s" % execname)
    sys.exit(1)

def idle(statushistory, emotions):
#idle module contains functions that are performed when idling, depending on the state of the robot.
#functions are performed a bit differently depending on emotion.

   
    if statushistory.count("Ready")%12:
        displayEmotion(emotions)
        #print("customers attracted")
    
    if statushistory.count("Ready")%20:
        attractCustomers(emotions)
        #print("emotion displayed")


def attractCustomers(emotions):
    #TODO
    #mir_calls.add_to_mission_queue("3ac4fc26-3f3f-11e9-9822-94c691a3a93e")
    emotions.mod_emotion(0,-1)
    print("attracting customers")


def displayEmotion(emotions):
    print("displaying emotion")
    if emotions.get_emotion() in ("frustrated", "angry"):
        #TODO mir mission
        print("in frustrated or angry")
        print("my emotion is")
        print(emotions.get_emotion())
        emotions.mod_emotion(0,-1)
    elif emotions.get_emotion() in ("sad", "bored"):
        #TODO mir mission
        print("in sad or bored")
        print("my emotion is")
        print(emotions.get_emotion())
        emotions.mod_emotion(-1,-1)
    else:
        #TODO mir mission
        print("in happy excited or content")
        print("my emotion is")
        print(emotions.get_emotion())
        emotions.mod_emotion(-1,-1)