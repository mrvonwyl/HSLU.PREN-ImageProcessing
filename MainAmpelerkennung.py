import numpy as np
import cv2
import time
from TrafficLightDetection import *

print ('Start Traffic Light Detection')

# start the video capture
camera = cv2.VideoCapture(0)

# initialize booleans for traffic light detection
# loop: initial state TRUE to run the loop and FALSE to stop the loop
# traffic_light: initial state red = FALSE and green = TRUE
loop = True
traffic_light = False

# looping while video capture is active
while loop:
        # grab the current frame
        _, frame = camera.read()
        cv2.imshow('frame', frame)
        
        # prepare the frame for color detection
        frame = frame_prep(frame)

        # set the color for color detection and
        # create a mask by checking for red and green traffic lights
        mask = color_detection(frame, 'red')
        cv2.imshow('mask', mask)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        contour = contour_detection(mask)
        
        # give the go-signal when a matching contour was found
        traffic_light = go_time(contour)
        
        # display the original frame the mask amd the result of
        # overlaying the mask with the original frame           
        print (traffic_light)
        time.sleep(.5) 
        
        # stop the loop if it is go time
        if (traffic_light == True):
                loop = False

print ('Go Time')
cv2.release()
cv2.destroyAllWindows()
