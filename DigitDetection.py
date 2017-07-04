import time
import cv2
import numpy as np
from threading import Thread

from DigitIsolation import DigitIsolation as di
from DigitRecognition import DigitRecognition as dr

class DigitDetection(Thread):

    def run(self):
        cap = cv2.VideoCapture(0)

        while not self.cancelled:
            img = cv2.imread('images/150.jpg')

            # Capture frame-by-frame
            ret, frame = cap.read()

            if self.timedebug:
                time1 = int(round(time.time() * 1000))
            try:
                # print('start: ' + repr(0))

                img = frame
                if self.debug:
                    cv2.imshow("orig", img)

                resized = di.isolate_roman_digit(img, self.debug)
                if self.debug:
                    cv2.imshow('resized', resized)

                if self.timedebug:
                    time2 = int(round(time.time() * 1000))
                    print('isolated: ' + repr(time2 - time1))

                temp_number = dr.recognize_digit(resized, img, self.debug)

                if temp_number >= 1 and temp_number <= 5:
                    print(temp_number)
                    self.number[temp_number - 1] = self.number[temp_number - 1] + 1

                if self.timedebug:
                    time3 = int(round(time.time() * 1000))
                    print('recognized: ' + repr(time3 - time2))
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                i = 0
                # if self.timedebug:
                    # time3 = int(round(time.time() * 1000))

            print(self.number)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #time.sleep(.5)

        # When everything done, release the capture
        print("final numbers: " + repr(self.number))

        cap.release()
        cv2.destroyAllWindows()

    def getNumber(self):
        if self.number.max() == 0:
            return 0
        else:
            return self.number.argmax(axis=0) + 1

    def cancel(self):
        self.cancelled = True

    def __init__(self):
        super(DigitDetection, self).__init__()
        self.cancelled = False
        self.debug = False
        self.timedebug = True
        self.number = np.array([0, 0, 0, 0, 0], np.uint16)
