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

    status = mir_calls.get_mir_status()

    if status == 'Executing':
         print("we are on a mission")

    if status == 'Ready':
         print("we are not on a mission anymore")

    return status
