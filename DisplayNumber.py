import RPi.GPIO as GPIO
import time
from random import randint


class DisplayNumber:
    global empCount
    empCount = 0
    global segments
    segments = (17, 27, 22, 10, 24, 23, 18)
    global num
    num = {' ':(1,1,1,1,1,1,1),
           '0':(0,1,0,0,0,0,0),
           '1':(1,1,1,1,1,0,0),
           '2':(1,0,0,0,0,0,1),
           '3':(1,0,1,0,0,0,0),
           '4':(0,0,1,1,1,0,0),
           '5':(0,0,1,0,0,1,0),
           '6':(0,0,0,0,0,1,0),
           '7':(1,1,1,0,1,0,0),
           '8':(0,0,0,0,0,0,0),
           '9':(0,0,1,0,0,0,0)}

    def __init__(self, number):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        global segments
        global num
        # alles einschalten
        self.everythingOn()
        time.sleep(1)
        self.everythingOff()

    def displayDigit(self, number):
        #Sicherheit, falls irgend ein Wert > 5 gemeldet wird.
        if number>5:
            number=randint(0,5)
        #print "Folgende Nummer wird angezeigt" + str(number)
        for loop in range(0, 7):
            GPIO.output(segments[loop], num[str(number)][loop])
            #time.sleep(2)

    def blink(self,count):
        for number in range(0,count):
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
