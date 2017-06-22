import time
from operator import itemgetter

import cv2, math
import numpy as np

from DigitIsolation import DigitIsolation

class DigitRecognition:

    @staticmethod
    def recognize_digit(img):
        number = 0

        _, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        angles = []

        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            # print('epsilon: ' + repr(epsilon))

            if epsilon >= 1:
                _, _, angle = cv2.fitEllipse(cnt)
                angles.append(angle)

        print('angles: ' + repr(angles))

        if len(angles) == 1:
            number = 1
        elif len(angles) == 2:
            angledif = abs(angles[0] - angles[1])
            if angledif < 12:
                number = 2
            else:
                number = 5
        elif len(angles) == 3:
            angledif1 = abs(angles[0] - angles[1])
            angledif2 = abs(angles[0] - angles[2])

            if angledif1 < 12 and angledif2 < 12:
                number = 3
            else:
                number = 4

        return number
