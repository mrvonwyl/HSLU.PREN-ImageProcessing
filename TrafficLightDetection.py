from collections import deque
import numpy as np
import imutils
import cv2

class TrafficLightDetection
        #returns the numpy array for the color red in the hsv color space
        def color_value(color):
                if (color == 'red'):
                        color = np.array([170, 100, 100],
                                         [180, 255, 255],
                                         [  0, 100, 100],
                                         [ 10, 255, 255])
                
                elif (color == 'green'):
                        color = np.array([170, 100, 100],
                                         [180, 255, 255])
                return color

        # returns a resized, blurred and HSV color space converted frame 
        def frame_prep():
                frame = imutils.resize(frame, width = 600)
                frame = cv2.GaussianBlur(frame, (11, 11), 0)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                return frame

        # detects the given color and creates a bit mask for said color               
        def color_detection(traffic_light, frame, color):
        
        	# checking the state of the traffic light
        	if not (traffic_light):
        	
        		# construct a mask for the given color,
        		# then perform a series of dilations and erosions to
        		# remove any small blobs left in the mask
                	#mask_top = cv2.inRange(frame, lower_red_top, upper_red_top)
                	mask_top = cv2.inRange(frame, color[0, 0:2], color[1, 0:2])
        		mask_top = cv2.erode(mask_top, None, iterations = 2)
                	mask_top = cv2.dilate(mask_top, None, iterations = 2)
        	
                	# construct a mask for the bottom bound of the HSV color "red",
                        # then perform a series of dilations and erosions to
                	# remove any small blobs left in the mask
        		#mask_bottom = cv2.inRange(hsv, lower_red_bottom, upper_red_bottom)
        		mask_bottom = cv2.inRange(frame, color[2, 0:2], color[3, 0:2])
        		mask_bottom = cv2.erode(mask_bottom, None, iterations = 2)
        		mask_bottom = cv2.dilate(mask_bottom, None, iterations = 2)     
        
        		# combine the top and bottom masks to create the complete mask
        		mask = cv2.add(mask_top, mask_bottom)
        		
                return mask

        # returns the found contours in the given mask
        def contour_detection(mask):
                contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                return contour

        # returns the constraints for the contours
        def contour_constraints():
                return constraints

        # returns true or false wether the contours match the given constraints
        def go_time(contour);
                if len(contour) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and centroid
		c = max(contour, key = cv2.contourArea)
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
				return False
			
			else:
				# when the traffic light is FALSE then set it to TRUE
				return True
			
			print (traffic_light)
			time.sleep(.5) 
