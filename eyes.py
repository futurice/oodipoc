#!/usr/bin/env python

import serial
import sys
import time

global ser
#remember to check if port is correct
try:
    ser = serial.Serial("/dev/ttyACM0",baudrate=19200, timeout = 1)
except serial.SerialException:
    print("Error: Arduino not available at ttyACM0")

def lookRight():
    print("I look right")
    ser.write(bytes("800", encoding="ascii"))
    time.sleep(2)

def lookLeft():
    print("I look left")
    ser.write(bytes("-800", encoding="ascii"))
    time.sleep(2)

def lookDown():
    print("I look down")
    ser.write(bytes("0", encoding="ascii"))
    time.sleep(2)

def lookUp():
    print("I look up")
    ser.write(bytes("1600", encoding="ascii"))
    time.sleep(2)

def rollEyes():
    print("Rolling eyes")
    ser.write(bytes("5000", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("0", encoding="ascii"))
    time.sleep(2)

def rollEyesAchoo():
    print("Rolling eyes")
    ser.write(bytes("5000", encoding="ascii"))
    time.sleep(2.5)
    ser.write(bytes("0", encoding="ascii"))
    time.sleep(2)

def topRoll():
    print("Toproll!")
    ser.write(bytes("1900", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("1300", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("1900", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("1300", encoding="ascii"))
    time.sleep(2)
    ser.write(bytes("0", encoding="ascii"))
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
