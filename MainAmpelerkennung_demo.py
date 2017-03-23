from collections import deque
import time
import numpy as np
import imutils
import cv2

# start the video capture
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture('videos/AmpelTest.mp4')

# initialize boolean for the traffic light
# initial state red = FALSE and green = TRUE
traffic_light = False

# define range of red color in HSV (Hue, Saturation, Value)
lower_red_top = np.array([170, 100, 100])
upper_red_top = np.array([180, 255, 255])
lower_red_bottom = np.array([  0, 100, 100])
upper_red_bottom = np.array([ 10, 255, 255])

# define range of green color in HSV (Hue, Saturation, Value)
lower_green = np.array([45, 100, 100])
upper_green = np.array([75, 255, 255])
    
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen = 32)

# looping while video capture is active
while True:
	# grab the current frame
	_, frame = camera.read()
	# frame = cv2.imread('images/color_gradient.png')
	
	# resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width = 600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	# checking the state of the traffic light
	if not (traffic_light):
	
		# construct a mask for the top bound of the HSV color "red",
		# then perform a series of dilations and erosions to
		# remove any small blobs left in the mask
		mask_top = cv2.inRange(hsv, lower_red_top, upper_red_top)
		mask_top = cv2.erode(mask_top, None, iterations = 2)
		mask_top = cv2.dilate(mask_top, None, iterations = 2)
	
		# construct a mask for the bottom bound of the HSV color "red",
		# then perform a series of dilations and erosions to
		# remove any small blobs left in the mask
		mask_bottom = cv2.inRange(hsv, lower_red_bottom, upper_red_bottom)
		mask_bottom = cv2.erode(mask_bottom, None, iterations = 2)
		mask_bottom = cv2.dilate(mask_bottom, None, iterations = 2)

		# combine the top and bottom masks to create the complete mask
		mask = cv2.add(mask_top, mask_bottom)
	
	else:
		# construct a mask for HSV color "green",
		# then perform a series of dilations and erosions to
		# remove any small blobs left in the mask
		mask = cv2.inRange(hsv, lower_green, upper_green)
		mask = cv2.erode(mask, None, iterations = 2)
		mask = cv2.dilate(mask, None, iterations = 2)
		
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

			
	# update the points queue
	pts.appendleft(center)
	
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# Bitwise-AND mask and original image	
	res = cv2.bitwise_and(frame, frame, mask = mask)
		
	# display the original frame the mask amd the result of ovelaying
	# the mask with the original frame		
	cv2.imshow('frame',frame)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)
	
	# stop the script by pressing 'q'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# cv2.release()
cv2.destroyAllWindows()