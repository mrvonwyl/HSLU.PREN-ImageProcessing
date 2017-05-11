from collections import deque
import numpy as np
import imutils
import cv2

# returns a resized, blurred and HSV color space converted frame
def frame_prep(frame):
        frame = imutils.resize(frame, width = 600)
        frame = frame[200:500, 50:200]
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        return frame

# detects the given color and creates a bit mask for said color
def color_detection(frame, color):

        if (color == 'red'):
                top_min = np.array([170, 50, 50])
                top_max = np.array([180, 255, 255])
                bottom_min = np.array([  0, 50, 50])
                bottom_max = np.array([ 10, 255, 255])

        elif (color == 'green'):
                top = np.array([170, 100, 100])
                bottom = np.array([170, 100, 100])

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
        return mask

# returns the found contours in the given mask
def contour_detection(mask):
        contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        return contour

# returns TRUE or FALSE wether the contours match the given constraints
def go_time(contour):

        # only proceed if at least one contour was found
        if len(contour) > 0:

                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and centroid
                c = max(contour, key = cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum and maximum size
                if (radius > 10 and radius < 15):
                        return 'pg'
                else:
                        return 'ps'
        else:
                return 'ps'
