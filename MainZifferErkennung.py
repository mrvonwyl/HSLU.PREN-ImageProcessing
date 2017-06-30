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

number = 0

while number == 0:
    img = cv2.imread('images/150.jpg')

    # Capture frame-by-frame
    ret, frame = cap.read()

    time1 = int(round(time.time() * 1000))
    try:
        print('start: ' + repr(0))

        # img = frame
        cv2.imshow("orig", img)

        resized = di.isolate_roman_digit(img)
        cv2.imshow('resized', resized)

        time2 = int(round(time.time() * 1000))
        print('isolated: ' + repr(time2 - time1))

        number = dr.recognize_digit(resized)

        time3 = int(round(time.time() * 1000))
        print('recognized: ' + repr(time3 - time2))
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        time3 = int(round(time.time() * 1000))
        print('error: ' + repr(time3 - time1))

    print(number);

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # time.sleep(.500)
    number = 0

# When everything done, release the capture
print("final number");
print(number);

cap.release()
cv2.destroyAllWindows()
