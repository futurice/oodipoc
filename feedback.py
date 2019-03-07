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

def feedback(emotions, isReceived,feedback):
#advise module checks the location of advising, and acts upon that. 

   
    if isReceived==0:
        askForFeedback()
        #print("customers attracted")
    
    if isReceived==1:
        feedbackReceived(emotions,feedback)
        #print("emotion displayed")


def askForFeedback():
    #TODO mir mission to roll a bit forward
    #TODO flask call display feedback screen
    #TODO wait for 30 secs
    print("feedback asked for")


def feedbackReceived(emotions, feedback):
    #check if feedback is good or bad
    print("feedback received")

    if feedback == "good":
        #TODO flask call shut off screen
        if emotions.get_emotion() in ("excited","happy","content","bored"):
            #TODO mir mission
            print("displayed extremely happy")
        else:
            #TODO mir mission
            print("displayed kind of happy")
        emotions.mod_emotion(+3,+3)

    elif feedback == "bad":
        #TODO flask call shut off screen
        if emotions.get_emotion() in ("excited","happy","content","bored"):
            #TODO mir mission
            print("displayed disappointed")
        elif emotions.get_emotion()=="sad":
            #TODO mir mission
            print("displayed sad")
        else:
            #TODO mir mission
            print("displayed angry")
        emotions.mod_emotion(-2,-2)