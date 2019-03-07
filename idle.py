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

#this is a test

    if emotions.get_emotion() == "bored":
        print("I am bored")
        if statushistory.count("Ready")==10:
            #mir_calls.add_to_mission_queue("3ac4fc26-3f3f-11e9-9822-94c691a3a93e")
            print("I AM SO SO BORED")
    
    if statushistory.count("Ready")==12:
        emotions.mod_emotion(0,-1)
        print("emotions were modded EXTREME BOREDOM")

    


"""
def idle():
    if (statushistory.count("ready")>20):
        emotions.set_emotion(-1)
        mir_emotions.little_boredom()
    elif (statushistory.count("ready")>40):
        emotions.set_emotion(-1)
        mir_emotions.big_boredom()
    else:
        return
"""