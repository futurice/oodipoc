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
import eyes
import random

import mir_calls
import emotions


def syntax(execname):
    print("Syntax: %s" % execname)
    sys.exit(1)

def idle(statushistory, emotions):
#idle module contains functions that are performed when idling, depending on the state of the robot.
#functions are performed a bit differently depending on emotion.

    percentage = random.random() * 100
    print("random activity percentage: " + str(percentage))

    if percentage < 20:
        displayEmotion(emotions)
    
    if percentage >= 20 and percentage < 40:
        attractCustomers(emotions)



def attractCustomers(emotions):
    """
    Randomize between:

    Two Achoo - https://freesound.org/people/Reitanna/sounds/343921/ 
    Scoot a bit back with each achoo, then roll slowly forward
    Roll eyes all the way around with each achoo
    Show purple light on achoo

    Random chirping - https://freesound.org/people/radarflora/sounds/350690/ 
    Roll around a bit
    Look around a bit
    Rainbow lights

    """
    
    #TODO

    reaction = random.random() * 100

    print("random reaction percentage: " + str(reaction))

    if reaction < 5:
        achoo()
        emotions.mod_emotion(2,2)

    if reaction >= 5 and reaction < 10:
        chirping()

    if reaction >= 10 and reaction < 20:
        eyes.lookRight()
        time.sleep(2)
        eyes.lookUp()
        time.sleep(3)
        eyes.lookDown()
    
    if reaction >= 20 and reaction < 50:
        eyes.lookLeft()
        time.sleep(1)
        eyes.lookRight()
        time.sleep(1)
        eyes.lookDown()

    if reaction >= 50:
        eyes.lookRight()
        time.sleep(3)
        eyes.lookDown()
        

    print("attracting customers")

def displayEmotion(emotions):

    """

    Frustrated or angry

    Annoyed beep - https://freesound.org/people/DontGoThere/sounds/255883/ (this should be slowed down)
    Show red lights
    Look left, look right


    Sad or bored

    Sad wobbling sound - https://freesound.org/people/pschrandt/sounds/428076/  (make sure this doesn’t play too loud)
    Look at ground
    Shake (as if shaking head)
    Show blue light


    Happy excited or content

    happy chirping (when content) - https://freesound.org/people/Illud/sounds/271674/ 
    Goes from side to side, looks to each side
    Show green light
    """

    print("displaying emotion")
    if emotions.get_emotion() in ("frustrated", "angry"):
        #TODO mir mission
        print("in frustrated or angry")
        print("my emotion is")
        print(emotions.get_emotion())
        emotionAngry()
        emotions.mod_emotion(0,-1)

    elif emotions.get_emotion() in ("sad", "bored"):
        #TODO mir mission
        print("in sad or bored")
        print("my emotion is")
        print(emotions.get_emotion())
        eyes.topRoll()
        emotions.mod_emotion(-1,-1)
        

    else:
        #TODO mir mission
        print("in happy excited or content")
        print("my emotion is")
        print(emotions.get_emotion())
        eyes.topRoll()
        emotions.mod_emotion(-1,-1)

def achoo():
    mir_calls.add_to_mission_queue("f747a369-509c-11e9-9b99-94c691a3a93e")
    eyes.rollEyesAchoo()

def chirping():
    mir_calls.add_to_mission_queue("17f74b3b-5b99-11e9-90b2-94c691a3a93e")

def emotionAngry():
    mir_calls.add_to_mission_queue("9cf49b99-5b9b-11e9-90b2-94c691a3a93e")
    time.sleep(0.2)
    eyes.lookRight()
    eyes.lookLeft()
    eyes.lookDown()
