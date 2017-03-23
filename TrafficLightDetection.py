import numpy as np
import cv2

def color_detection(traffic_light, hsv):
	# define range of red color in HSV (Hue, Saturation, Value)
	lower_red_top = np.array([170, 100, 100])
	upper_red_top = np.array([180, 255, 255])
	lower_red_bottom = np.array([  0, 100, 100])
	upper_red_bottom = np.array([ 10, 255, 255])
	
	# define range of green color in HSV (Hue, Saturation, Value)
	lower_green = np.array([45, 100, 100])
	upper_green = np.array([75, 255, 255])

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
	
	return mask