import numpy as np
import cv2
import time


print ('Start Traffic Light Detection')
loop = True
# start the video capture
camera = cv2.VideoCapture(0)

boundaries = [
    ([65, 70, 240], [80, 90, 255])]

# looping while video capture is active

while loop:
    # grab the current frame
    _, frame = camera.read()
    cv2.imshow('frame', frame)
    frame = frame[0:100, 0:100]

    # loop over the boundariesq
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask = mask)

        # show the images
        cv2.imshow("images", np.hstack([frame, output]))
        gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
        cv2.imshow("test",gray)
        contour = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(contour) > 0:
        print ("gogogo")




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break