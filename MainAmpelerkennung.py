from collections import deque
import time
import numpy as np
import imutils
import cv2
from TrafficLightDetection import color_detection

# start the video capture
camera = cv2.VideoCapture(0)

# initialize boolean for the traffic light
# initial state red = FALSE and green = TRUE
traffic_light = False

# looping while video capture is active
while True:
	# grab the current frame
	_, frame = camera.read()
	
	# resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width = 600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	# create a mask by checking for red and green traffic lights
	mask = color_detection(traffic_light, hsv)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key = cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

			#change the state of the traffic light
			if (traffic_light):
				# when the traffic light is TRUE then set it to FALSE
				traffic_light = False
			
			else:
				# when the traffic light is FALSE then set it to TRUE
				traffic_light = True
			
			print (traffic_light)
			time.sleep(.5)
	
	# display the original frame the mask amd the result of ovelaying
	# the mask with the original frame		
	cv2.imshow('frame',frame)
	cv2.imshow('mask', mask)
	
	# stop the script by pressing 'q'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.release()
cv2.destroyAllWindows()