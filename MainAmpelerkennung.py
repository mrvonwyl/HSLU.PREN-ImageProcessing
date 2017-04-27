import numpy as np
import cv2
from TrafficLightDetection import *

# start the video capture
camera = cv2.VideoCapture(0)

# initialize boolean for the traffic light
# initial state red = FALSE and green = TRUE
traffic_light = False

# looping while video capture is active
while True:
	# grab the current frame
	_, frame = camera.read()

        #set the color for color detection
	color = color_vallue('red')
	
	# prepare the frame for color detection
	frame = frame_prep()
	
	# create a mask by checking for red and green traffic lights
	mask = color_detection(traffic_light, frame, color)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	contour = contour_detection(mask)
	
	# give the go-signal when a matching contour was found
	traffic_light = go_time(contour)
	
	# display the original frame the mask amd the result of overlaying
	# the mask with the original frame		
	cv2.imshow('frame',frame)
	cv2.imshow('mask', mask)
	
	# stop the script by pressing 'q'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.release()
cv2.destroyAllWindows()
