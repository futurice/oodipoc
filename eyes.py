#!/usr/bin/env python

import serial
import sys
import time

global ser
#remember to check if port is correct
ser = serial.Serial("/dev/cu.usbmodem1441",baudrate=19200, timeout = 1)

def lookLeft():
    ser.write(bytes("800", encoding="ascii"))
    print("I looked left")
    time.sleep(2)
    #ser.close()

def lookRight():
    ser.write(bytes("-800", encoding="ascii"))
    print("I looked right")
    time.sleep(2)
    #ser.close()

def lookDown():
    ser.write(bytes("0", encoding="ascii"))
    print("I looked down")
    time.sleep(2)

def lookUp():
    ser.write(bytes("1600", encoding="ascii"))
    print("I looked up")
    time.sleep(2)

def rollEyes():
    ser.write(bytes("5000", encoding="ascii"))
    print("I looked up")
    time.sleep(2)
    ser.write(bytes("0", encoding="ascii"))
    time.sleep(2)

def topRoll():
    ser.write(bytes("1900", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("1300", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("1900", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("1300", encoding="ascii"))
    time.sleep(2)

def eyesInput(): 
    arduinoWrite = input("give me a number:")
    print(arduinoWrite)
    ser.write(bytes(arduinoWrite, encoding="ascii"))
    print("sent data")

#main loop for testing
def main():
    time.sleep(2)
    #lookLeft()
    #lookRight()
    #lookUp()
    #lookDown()
    rollEyes()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()