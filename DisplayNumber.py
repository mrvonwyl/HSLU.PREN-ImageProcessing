import RPi.GPIO as GPIO
import time
from random import randint


class DisplayNumber:
    global empCount
    empCount = 0
    global segments
    segments = (12, 13, 16, 19, 20, 21, 26)
    global num
    num = {' ': (1, 1, 1, 1, 1, 1, 1),
           '0': (0, 0, 0, 1, 0, 0, 0),
           '1': (1, 1, 0, 1, 1, 0, 1),
           '2': (0, 1, 0, 0, 0, 1, 0),
           '3': (0, 1, 0, 0, 1, 0, 0),
           '4': (1, 0, 0, 0, 1, 0, 1),
           '5': (0, 0, 1, 0, 1, 0, 0),
           '6': (0, 0, 1, 0, 0, 0, 0),
           '7': (0, 1, 0, 1, 1, 0, 1),
           '8': (0, 0, 0, 0, 0, 0, 0),
           '9': (0, 0, 0, 0, 1, 0, 0)}

    def __init__(self, number):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        global segments
        global num
        # alles einschalten
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
            #print segment

        time.sleep(1)

        # alles ausschalten
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)
            #print segment

    def displayCount(self, number):
        #Sicherheit, falls irgend ein Wert > 5 gemeldet wird.
        if number>5:
            number=randint(0,5)
        #print "Folgende Nummer wird angezeigt" + str(number)
        for loop in range(0, 7):
            GPIO.output(segments[loop], num[str(number)][loop])
            #time.sleep(2)

    def everythingOff(self):
        # alles ausschalten
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)
            #print segment
