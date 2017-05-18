#!/usr/bin/env python

import time
import serial


class Serial:
    global ser


    def __init__(self, number):
        ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    def sendText(self, text):
        ser.write(text)
        time.sleep(1)

