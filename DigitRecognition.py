import time
from operator import itemgetter

import cv2, math
import numpy as np

from DigitIsolation import DigitIsolation

class DigitRecognition:

    @staticmethod
    def recognize_digit(img):
        number_found = False
        number = 0


        # Höhe von Bild auslesen
        height, width = img.shape[:2]

        # Alle Corners in Bild finden.
        corners = cv2.goodFeaturesToTrack(img, 10000, 0.0001, 10) # faktor ist 10 / 570
        draw_im = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        arr_oben = []
        arr_unten = []
        arr_all = []

        # wenn 4 Corners == 1
        # wenn 8 Corners = 2 oder 5
        # wenn 12 Corners = 3 oder 4

        for i in corners:
            # draws on corners
            x, y = i.ravel()

            # Nur Corners am oberen oder unteren Rand auswählen
            #5% ausrechnen
            top10proz = height * 0.05
            if y < top10proz:
                arr_oben.append([x, y])
                arr_all.append([x, y])
                cv2.circle(draw_im, (x, y), 10, (0, 0, 255), 2)
            if y > (height-top10proz):
                arr_unten.append([x, y])
                arr_all.append([x, y])
                cv2.circle(draw_im, (x, y), 10, (0, 0, 255), 2)

        arr_unten = sorted(arr_unten, key=itemgetter(0))
        arr_oben = sorted(arr_oben, key=itemgetter(0))

        print('ARR')
        print(arr_all.__len__())

        if len(arr_all) == 12:
            print(12)
            distX5X4Oben = arr_oben[4][0] - arr_oben[3][0]
            distX5X4Unten = arr_unten[4][0] - arr_unten[3][0]
            verhaeltnisX4 = distX5X4Oben - distX5X4Unten
            ################################################################################
            # Hier aufpassen
            # Diese Rechnung ist noch nicht verlässlich
            # müssten hier noch eine Logik finden wie man das verhältniss einstuffen soll
            ################################################################################
            if verhaeltnisX4 < (width * 0.2) and verhaeltnisX4 > (width * -0.2):
                number = 3
            else:
                number = 4

        if len(arr_all) == 8:
            print(8)
            distX3X2Oben = arr_oben[2][0] - arr_oben[1][0]
            distX3X2Unten = arr_unten[2][0] - arr_unten[1][0]
            verhaeltnissX2 = distX3X2Oben - distX3X2Unten
            if verhaeltnissX2 < 100 and verhaeltnissX2 > -100:
                number = 2
            else:
                number = 5

        if len(arr_all) == 4:
            print(4)
            number = 1

        return number
