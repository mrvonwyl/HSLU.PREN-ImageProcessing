import time
import serial
from threading import Thread

class SerialRead(Thread):

    def run(self):
        print("Serial Read Init")
        while not self.cancelled:
            x = self.ser.readline()
            if x.__len__() != 0:
                self.msg = x
                print('serial: ' + repr(self.msg))

    def __init__(self):
        super(SerialRead, self).__init__()
        self.cancelled = False
        self.msg = 0
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    def getMsg(self):
        return self.msg

    def cancel(self):
        print("canceled")
        self.cancelled = True

