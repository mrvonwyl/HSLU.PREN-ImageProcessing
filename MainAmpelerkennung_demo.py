from collections import deque
import cv2
import numpy as np
import imutils
import time

#def start_traffic_light_detection():
print('Start Capture')

# start the video capture
#camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture('videos/AmpelTest.mp4')

# initialize variables for traffic light detection
# loop: initial state TRUE to run the loop and FALSE to stop the loop
# traffic_light: initial state red = FALSE and green = TRUE
# emergency_counter: a counter to prevent the pink panzer form never starting
# even if no signal from the traffic light can be detected
loop = True
traffic_light = 'ps'
emergency_counter = 0

# looping while video capture is active
if (camera.isOpened()):
	while (True):

		# if the counter reaches 500, the go siganl will be given
		# regardless of the traffic light
		if (emergency_counter < 500):

			print (traffic_light)
			
			# grab the current frame
			_, frame = camera.read()
			
			# prepare the frame for color detection
			frame = imutils.resize(frame, width = 600)
			frame_re = frame[300:600, 200:300]
			frame = cv2.GaussianBlur(frame, (11, 11), 0)
			#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			cv2.imshow('frame', frame)

			# set the color for color detection and create
			# a mask by checking for red traffic lights
			top_min = np.array([170, 50, 50])
			top_max = np.array([180, 255, 255])
			bottom_min = np.array([  0, 50, 50])
			bottom_max = np.array([ 10, 255, 255])

			# construct a mask for the given color,
			# then perform a series of dilations and erosions to
			# remove any small blobs left in the mask
			#mask_top = cv2.inRange(frame, lower_red_top, upper_red_top)
			mask_top = cv2.inRange(frame, top_min, top_max)
			mask_top = cv2.erode(mask_top, None, iterations = 2)
			mask_top = cv2.dilate(mask_top, None, iterations = 2)

			# construct a mask for the bottom bound of the HSV color "red",
			# then perform a series of dilations and erosions to
			# remove any small blobs left in the mask
			#mask_bottom = cv2.inRange(hsv, lower_red_bottom, upper_red_bottom)
			mask_bottom = cv2.inRange(frame, bottom_min, bottom_max)
			mask_bottom = cv2.erode(mask_bottom, None, iterations = 2)
			mask_bottom = cv2.dilate(mask_bottom, None, iterations = 2)

			# combine the top and bottom masks to create the complete mask
			mask = cv2.add(mask_top, mask_bottom)
			cv2.imshow('mask', mask)

			# find contours in the mask and initialize the current
			# (x, y) center of the ball
			contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			
			# give the go-signal when a matching contour was found
			# only proceed if at least one contour was found.
			if len(contour) > 0:

				# find the largest contour in the mask, then use
				# it to compute the minimum enclosing circle and centroid
				c = max(contour, key = cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				# only proceed if the radius meets a minimum and maximum size
				if (radius > 10 and radius < 15):
					traffic_light = 'pg'
				else:
					traffic_light = 'ps'
			else:
				traffic_light = 'ps'         
			
			# stop the loop if it is go time
			if (traffic_light == 'pg'):
				print (traffic_light)
				print ('Green Light detected')
				loop = False
				
			# increase the emergency counter
			emergency_counter += 1

			cv2.imshow('frame', frame)
			cv2.imshow('frame_re', frame_re)
			cv2.imshow('mask', mask)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		else:
			# stop the loop if the emergency counter reaches 100
			# and set the traffic light variable accordingly                        
			traffic_light = 'pg'
			loop = False
			print (traffic_light)
			print ('Emergency Loop exeeded')

			cv2.imshow('frame', frame)
			cv2.imshow('frame_re', frame_re)
			cv2.imshow('mask', mask)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
else:
	print('No Video Capture detected')

print ('Go Time')
camera.release()
cv2.destroyAllWindows()
#return traffic_light
