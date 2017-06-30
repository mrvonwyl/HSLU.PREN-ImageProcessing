import time
import cv2
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

            time1 = int(round(time.time() * 1000))
            try:
                print('start: ' + repr(0))

                img = frame
                cv2.imshow("orig", img)

                resized = di.isolate_roman_digit(img)
                cv2.imshow('resized', resized)

                time2 = int(round(time.time() * 1000))
                print('isolated: ' + repr(time2 - time1))

                self.number = dr.recognize_digit(resized)

                time3 = int(round(time.time() * 1000))
                print('recognized: ' + repr(time3 - time2))
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                time3 = int(round(time.time() * 1000))
                print('error: ' + repr(time3 - time1))

            print(self.number)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # time.sleep(.500)
            number = 0

        # When everything done, release the capture
        print("final number: " + repr(number))

        cap.release()
        cv2.destroyAllWindows()

    def getNumber(self):
        return self.number

    def cancel(self):
        self.cancelled = True

    def __init__(self):
        super(DigitDetection, self).__init__()
        self.cancelled = False
        self.number = 0