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

def syntax(execname):
    print("Syntax: %s" % execname)
    sys.exit(1)

def move():

     """
     “Bling” follow me - https://freesound.org/people/newagesoup/sounds/350359/ 



     Good

     Excited happy content or bored

     Happy acknowledgement - https://freesound.org/people/plasterbrain/sounds/242855/ 
     Move around a bit, flash rainbow lights


     Else

     Happy acknowledgement - https://freesound.org/people/plasterbrain/sounds/242855/ 


     Bad

     Excited happy content or bored

     Not that great feedback “doop” - https://freesound.org/people/Intimidated/sounds/74233/
     Look down
     Flash blue lights

     Sad

     Sad wobbling sound - https://freesound.org/people/pschrandt/sounds/428076/ 
     “Shake head”
     Look down
     Flash blue lights


     Else (angry)

     Confused sound - https://freesound.org/people/RICHERlandTV/sounds/352378/ 
     “Shake head”
     Look around 
     Flash red lights

     """

    status = mir_calls.get_mir_status()

    if status == 'Executing':
         print("debug: we are on a mission")

    if status == 'Ready':
         print("debug: we are not on a mission anymore")

    return status
