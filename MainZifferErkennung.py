import time

import cv2

from DigitIsolation import DigitIsolation

img = cv2.imread('images/4.png')

cap = cv2.VideoCapture('images/v2.webm')
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # img = frame
    cv2.imshow("orig", img)
    resized = DigitIsolation.isolate_roman_digit(img)
    cv2.imshow('resized', resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
