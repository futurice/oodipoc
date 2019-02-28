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

def idle(counter):

    status = mir_calls.get_mir_status()

    if status == 'Ready':
         print("we are not on a mission anymore")
         if counter==10:
               mir_calls.add_to_mission_queue("6de599b2-3b4a-11e9-9f5c-94c691a3a93e")

    return status
