import time
from operator import itemgetter

import cv2, math
import numpy as np

from DigitIsolation import DigitIsolation

class DigitRecognition:

    @staticmethod
    def recognize_digit(img, orig, debug):
        number = 0

        img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        _, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        angles = []

        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            # print('epsilon: ' + repr(epsilon))

            if epsilon >= 1:
                _, _, angle = cv2.fitEllipse(cnt)
                if debug:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(img2, [box], 0, (angle, 127, 0), 2)

                angles.append(angle)

        if debug:
            cv2.imshow('eli', img2)

        print('angles: ' + repr(angles))

        if number != 0:
            fn = '/tmp/imgs/' + str(int(round(time.time() * 1000))) + '.jpg'
            cv2.imwrite(fn, orig)
            print("image save as: " + fn)

        a1 = 12
        a2 = 168

        if len(angles) == 1:
            number = 1
        elif len(angles) == 2:
            angledif = abs(abs(angles[0] - angles[1]))
            print(angledif)
            if angledif < a1 or angledif > a2:
                number = 2
            else:
                number = 5
        elif len(angles) == 3:
            angledif1 = abs(abs(angles[0] - angles[1]))
            angledif2 = abs(abs(angles[0] - angles[2]))

            if (angledif1 < a1 or angledif1 > a2) and (angledif2 < a1 or angledif2 > a2):
                number = 3
            else:
                number = 4

        return number
