import time

import cv2

from DigitIsolation import DigitIsolation as di
from DigitRecognition import DigitRecognition as dr

cap = cv2.VideoCapture(1)

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

number = 0

while number == 0:
    img = cv2.imread('images/32.jpg')

    # Capture frame-by-frame
    ret, frame = cap.read()

    try:
        # img = frame
        cv2.imshow("orig", img)

        resized = di.isolate_roman_digit(img)
        cv2.imshow('resized', resized)

        number = dr.recognize_digit(resized)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
       print("Error");

    print(number);

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)
    number = 0

# When everything done, release the capture
print("final number");
print(number);

cap.release()
cv2.destroyAllWindows()
