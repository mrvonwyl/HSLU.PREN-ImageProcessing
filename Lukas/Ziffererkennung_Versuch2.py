import time
from operator import itemgetter

import cv2, math
import numpy as np

from DigitIsolation import DigitIsolation

img = cv2.imread('../images/4.png')

cap = cv2.VideoCapture('../images/v2.webm')

numbFound=False
while(numbFound==False):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # img = frame
    cv2.imshow("orig", img)
    resized = DigitIsolation.isolate_roman_digit(img)
    cv2.imshow('resized', resized)

    # Höhe von Bild auslesen
    height, width = resized.shape[:2]

    # Alle Corners in Bild finden.
    corners = cv2.goodFeaturesToTrack(resized, 10000, 0.0001, 10)
    draw_im = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    arrOben = []
    arrUnten = []
    arrAll = []
    # Wenn 4 Corners == 1
    # Wenn 8 Corners = 2 oder 5
    # Wenn 12 Corners = 3 oder 4
    for i in corners: #draws on corners
        x,y = i.ravel()

        # Nur Bilder am oberen oder unteren Rand auswählen
        if(y<10):
            arrOben.append([x,y])
            arrAll.append([x,y])
            cv2.circle(draw_im,(x,y), 10, (0,0,255), 2)
        if(y>(height-10)):
            arrUnten.append([x,y])
            arrAll.append([x,y])
            cv2.circle(draw_im,(x,y), 10, (0,0,255), 2)

    arrUnten=sorted(arrUnten, key=itemgetter(0))
    arrOben=sorted(arrOben, key=itemgetter(0))



    if(len(arrAll)==12):
        distX5X4Oben=arrOben[4][0]-arrOben[3][0]
        distX5X4Unten=arrUnten[4][0]-arrUnten[3][0]
        verhaeltnissX4=distX5X4Oben-distX5X4Unten
        if(verhaeltnissX4)<100 and verhaeltnissX4 > -100:
            print ("3 gefunden")
            numbFound=True
        else:
            print("4 gefunden")
            numbFound=True
    if(len(arrAll)==8):
        distX3X2Oben=arrOben[2][0]-arrOben[1][0]
        distX3X2Unten=arrUnten[2][0]-arrUnten[1][0]
        verhaeltnissX2=distX3X2Oben-distX3X2Unten
        if(verhaeltnissX2)<100 and verhaeltnissX2 > -100:
            print ("2 gefunden")
            numbFound=True
        else:
            print("5 gefunden")
            numbFound=True

    if(len(arrAll)==4):
        print("1 gefunden")
        numbFound=True

    cv2.imshow('resized2', draw_im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
