import time

import cv2

from DigitIsolation import DigitIsolation as di
from DigitRecognition import DigitRecognition as dr

cap = cv2.VideoCapture(0)

# cap.set(3, 1280)
# cap.set(4, 720)
# brightness
# cap.set(11, 2000)
# exposure
# cap.set(16, -10)
# contrast
# cap.set(12, 10)
# gain
# cap.set(15, -10)
# FPS
# cap.set(6, 0.1)

number = 1

while number > 0:
    img = cv2.imread('images/3.jpg')

    # Capture frame-by-frame
    ret, frame = cap.read()
    img = frame

    cv2.imshow('asd', img)
    fn = '/tmp/imgs/' + repr(number) + '.jpg'
    print(fn)
    cv2.imwrite(fn, img)

    number += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.100)

cap.release()
cv2.destroyAllWindows()
