import threading

import multiprocessing
import time

from DisplayNumber import DisplayNumber
from AmpelMain import MainAmpelerkennung
from DigitDetection import DigitDetection
from SerialRead import SerialRead
from Serial import Serial
from random import randint


class PinkPanzer:
    readyToStart = 0
    recognizedNumber = 0

    def __init__(self):
        print("init pinkpanzer")

    def main():
        dn = DisplayNumber()
        dd = DigitDetection()
        ampel = MainAmpelerkennung()
        sRead = SerialRead()
        ser = Serial()
        process2 = multiprocessing.Process(target=ampel.detect_light)

        dn.start()
        dd.start()
        sRead.start()

        process2.start()



        finish = False
        while not finish:
            msg = sRead.getMsg()
            if "F" in str(msg):
                #if msg == "b'Finish'":
                finish = True
                number = dd.getNumber()

                print("number main: " + str(number))

                if number == 0:
                    number = randint(1, 5)

                print("number main definitive: " + str(number))

                dd.cancel()
                dn.setNumber(number)
                dn.cancel()
                ser.sendText(str(number))
            time.sleep(0.5)
        print("pink panzer finish")

        #dn.everythingOff()

        #Bei Cancel wird letzte Blinken beendet und gegebene Zahl angezeigt



        #t_blink = threading.Thread(target=dn.blink())
        #t_blink.start()
        #ampel = MainAmpelerkennung()
        #t_ampel = threading.Thread(target=ampel.detect_light())
        #t_ampel.start()

    if __name__ == '__main__':
        main()
#Funktioniert für Ziffernanzeige aus anderer Klasse auf Raspberry
#from DisplayNumber import DisplayNumber
#import time
#DisplayNumber = DisplayNumber(1)
#DisplayNumber.displayCount(2)
#time.sleep(2)
#DisplayNumber.displayCount(8)
#time.sleep(2)
#DisplayNumber.everythingOff()
