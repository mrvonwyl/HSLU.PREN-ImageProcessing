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

        while not number_found:
            # Höhe von Bild auslesen
            height, width = img.shape[:2]

            # Alle Corners in Bild finden.
            corners = cv2.goodFeaturesToTrack(img, 10000, 0.0001, 10)
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

            if len(arr_all) == 12:
                distX5X4Oben = arr_oben[4][0] - arr_oben[3][0]
                distX5X4Unten = arr_unten[4][0] - arr_unten[3][0]
                verhaeltnissX4 = distX5X4Oben - distX5X4Unten
                ################################################################################
                # Hier aufpassen
                # Diese Rechnung ist noch nicht verlässlich
                # müssten hier noch eine Logik finden wie man das verhältniss einstuffen soll
                ################################################################################
                if verhaeltnissX4 < 100 and verhaeltnissX4 > -100:
                    number = 3
                    number_found = True
                else:
                    number = 4
                    number_found = True

            if len(arr_all) == 8:
                distX3X2Oben = arr_oben[2][0] - arr_oben[1][0]
                distX3X2Unten = arr_unten[2][0] - arr_unten[1][0]
                verhaeltnissX2 = distX3X2Oben - distX3X2Unten
                if verhaeltnissX2 < 100 and verhaeltnissX2 > -100:
                    number = 2
                    number_found = True
                else:
                    number = 5
                    number_found = True

            if len(arr_all) == 4:
                number = 1
                number_found = True

            cv2.imshow('resized2', draw_im)

            return number
