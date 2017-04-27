import time

import cv2

from DigitIsolation import DigitIsolation as di
from DigitRecognition import DigitRecognition as dr

img = cv2.imread('images/Nr4.png')

cap = cv2.VideoCapture('images/v2.webm')
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # img = frame
    cv2.imshow("orig", img)
    resized = di.isolate_roman_digit(img)

    number = dr.recognize_digit(resized)

    print(number);

    cv2.imshow('resized', resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
