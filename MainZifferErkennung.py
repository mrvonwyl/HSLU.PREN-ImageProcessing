import time

import cv2

from DigitIsolation import DigitIsolation as di
from DigitRecognition import DigitRecognition as dr

img = cv2.imread('images/33.jpg')

cap = cv2.VideoCapture(0)

# cap.set(3, 1280)
# cap.set(4, 720)
# brightness
# cap.set(11, 2000)
# exposure
cap.set(16, -10)
# contrast
# cap.set(12, 10)
# gain
# cap.set(15, -10)
# FPS
# cap.set(6, 0.1)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = frame
    cv2.imshow("orig", img)

    number = 0

    try:
        resized = di.isolate_roman_digit(img)
        cv2.imshow('resized', resized)
        number = dr.recognize_digit(resized)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Error");

    print(number);

    grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    cv2.imshow("grey", grey)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
