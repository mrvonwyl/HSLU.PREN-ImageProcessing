import numpy as np
import cv2,math

imgOrig = cv2.imread('E:/2s.jpg')


# cv2.inRange(img)

img = imgOrig

# define windows name
winName = "Display window"
# create new display window
window = cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
# resize window to specific size
cv2.resizeWindow(winName, 800, 450)
# display image
cv2.imshow(winName, img)

# cap = cv2.VideoCapture(0)
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # show the images
#     cv2.imshow("Capture", np.hstack([frame]))
#     #cv2.waitKey(0);
#
#     # Our operations on the frame come here
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Display the resulting frame
#     # cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# When everything done, release the capture
cv2.waitKey(0)
cv2.destroyAllWindows()