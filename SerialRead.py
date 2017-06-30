#!/usr/bin/env python

import time
import serial


class SerialRead:
    global ser
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 38400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

    def __init__(self):
        global ser

    def readSerial(self):
        print("Serial Read Init")
        while 1:
            x=ser.readline()
            if(x.__len__() != 0):
                print (x)

