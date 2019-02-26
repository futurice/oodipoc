#!/usr/bin/env python

"""
An emotion library for a robot.
"""

#from __future__ import print_function
    

class Emotion:

    def __init__(self, startemo, minemo, maxemo):
        self.current = startemo
        self.minimum = minemo
        self.maximum = maxemo

    def get_emotion(self):
        return self.current

    def set_emotion(self, new):
        self.current = self.current + new
        self.clamp(self.current, self.minimum, self.maximum)
        return self.current

    def clamp(self, current, minimum, maximum):
        self.current = max(min(self.maximum, self.current), self.minimum)
        return current
