from threading import Thread
from time import sleep


class threadedclass(Thread):
    global x
    def __init__(self):
        super(threadedclass, self).__init__()
        self.cancelled = False
        global x
        x=0
        # do other initialization here

    def run(self):
        """Overloaded Thread.run, runs the update
        method once per every 10 milliseconds."""
        print("start")
        while not self.cancelled:
            self.printX()
            sleep(0.1)
        print("letzeaktion vor cancel")

    def cancel(self):
        """End this timer thread"""
        print("canceled")
        self.cancelled = True

    def printX(self):
        print("X:"+str(x))

    def update(self,number):

        """Update the counters"""
        global x
        x=number
        print("Number: "+str(number))
        print("X: "+str(x))

    def getX(self):
        global x
        return x
