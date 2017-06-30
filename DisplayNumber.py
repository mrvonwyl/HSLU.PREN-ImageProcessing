from threading import Thread

import RPi.GPIO as GPIO
import time
from random import randint


class DisplayNumber(Thread):
    global empCount
    empCount = 0
    global segments
    segments = (17, 27, 22, 10, 24, 23, 18)
    global number
    global num
    num = {' ':(1,1,1,1,1,1,1),
        '0':(0,0,0,1,0,0,0),
        '1':(1,0,0,1,1,1,1),
        '2':(0,1,0,0,1,0,0),
        '3':(0,0,0,0,1,0,1),
        '4':(1,0,0,0,0,1,1),
        '5':(0,0,1,0,0,0,1),
        '6':(0,0,1,0,0,0,0),
        '7':(1,0,0,1,1,0,1),
        '8':(0,0,0,0,0,0,0),
        '9':(0,0,0,0,0,0,1)}

    def __init__(self):
        super(DisplayNumber, self).__init__()
        self.cancelled = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        global segments
        global num
        global number
        # alles einschalten
        self.everythingOn()
        time.sleep(1)
        self.everythingOff()

    def run(self):
        """Overloaded Thread.run, runs the update
        method once per every 10 milliseconds."""
        print("start")
        while not self.cancelled:
            time.sleep(0.01)
            self.blink()

        global number
        self.displayDigit(number)

        print("letze aktion vor cancel")


    def displayDigit(self, number):
        #Sicherheit, falls irgend ein Wert > 5 gemeldet wird.
        if number>5:
            number=randint(0,5)
        #print "Folgende Nummer wird angezeigt" + str(number)
        for loop in range(0, 7):
            GPIO.output(segments[loop], num[str(number)][loop])
            #time.sleep(2)

    def blink(self):
        self.everythingOff()
        time.sleep(0.5)
        self.everythingOn()
        time.sleep(0.2)
        self.everythingOff()
        time.sleep(0.1)
        self.everythingOn()
        time.sleep(0.2)


    def everythingOff(self):
        # alles ausschalten
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)
            #print segment

    # alles einschalten
    def everythingOn(self):
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
            #print segment

    def setNumber(self,l_number):
        global number
        number = l_number

    def cancel(self):
        """End this timer thread"""
        print("canceled")
        self.cancelled = True
