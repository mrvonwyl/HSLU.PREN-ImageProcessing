import threading

import multiprocessing
import time

from DisplayNumber import DisplayNumber
from AmpelMain import MainAmpelerkennung
from DigitDetection import DigitDetection
from SerialRead import SerialRead
from Serial import Serial


class PinkPanzer:
    readyToStart = 0
    recognizedNumber = 0

    def __init__(self):
        print("init pinkpanzer")
        # init kamera A
        # init ampelerkennung
        # init kamera Z
        # init ziffererkennung

        # Thread starten, welcher die Ziefferanzeige blinken lässt

        #mit t_blink.join() kann thread beendet werden

        # run ampelerkennung -> set readyToStart
        # send info to FMBD
        # run ziffererkennung -> set recognizedNumber
        # display number
        # send recognized number to FMBD

    def main():
        dn = DisplayNumber()
        dd = DigitDetection()
        ampel = MainAmpelerkennung()
        sRead = SerialRead()
        process2 = multiprocessing.Process(target=ampel.detect_light)
        process_readSerial = multiprocessing.Process(target=sRead.readSerial)

        dn.start()
        dd.start()

        process2.start()
        process_readSerial.start()

        numberFound= False
        while not numberFound:
            number = dd.getNumber()
            if(number != 0):
                numberFound=True
            time.sleep(0.1)
        print("Nummer gefunden in Main: "+str(number))
        dd.cancel()

        dn.setNumber(number)
        #dn.everythingOff()

        #Bei Cancel wird letzte Blinken beendet und gegebene Zahl angezeigt
        dn.cancel()
        ser = Serial()
        ser.sendText(str(number))

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
