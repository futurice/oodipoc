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

def advise(emotions, location, direction):
#advise module checks the location of advising, and acts upon that. 

   
    if location=="atShelf":
        atShelf(emotions)
        #print("customers attracted")
    
    if location=="atColumn":
        atColumn(emotions, direction)
        #print("emotion displayed")


def atShelf(emotions):
    #TODO mir mission to point at shelf
    #TODO flask call
    print("pointing at shelf")


def atColumn(emotions, direction):
    #check which direction the column is in and point there
    print("at column")

    if direction == "left":
        #TODO mir mission
        #TODO flask call
        print("pointed at column left")
        emotions.mod_emotion(+1,+1)

    elif direction == "right":
        #TODO mir mission
        #TODO flask call
        print("pointed at column right")
        emotions.mod_emotion(+1,+1)