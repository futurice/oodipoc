#!/usr/bin/env python

import serial
import sys
import time
#from common import clock, draw_str

#or should baud be 9600?

#ser = serial.Serial("/dev/cu.usbmodem1441",baudrate=19200, timeout = 1)
global ser
ser = serial.Serial("/dev/cu.usbmodem1441",baudrate=19200, timeout = 1)

def lookLeft():
    ser.write(bytes("800", encoding="ascii"))
    print("I looked left")
    time.sleep(2)
    #ser.close()

def lookRight():
    ser.write(bytes("-200", encoding="ascii"))
    print("I looked right")
    time.sleep(2)
    #ser.close()

def eyesTest(): 
    arduinoWrite = input("give me a number:")
    print(arduinoWrite)
    #print(type(arduinoWrite))
    ser.write(bytes(arduinoWrite, encoding="ascii"))
    print("sent data")

def main():
    time.sleep(2)
    #direction = str("-800")
    #print(type(direction))
    #ser.write(bytes(direction, encoding="ascii"))
    lookLeft()
    print("I did the function")
    lookRight()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        syntax(sys.argv[0])

    main()