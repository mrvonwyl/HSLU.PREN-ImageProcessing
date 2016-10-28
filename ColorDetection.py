import numpy as np
import cv2, math


def maskcolor(image, boundaries):
    lower = np.array(boundaries[0][0], dtype="uint8")
    upper = np.array(boundaries[0][1], dtype="uint8")
    return cv2.inRange(image, lower, upper)


def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape)/2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
    result = cv2.warpAffine(image, rot_mat, image.shape, flags=cv2.INTER_LINEAR)
    return result

img = cv2.imread('images/4wide.jpg')

blackBoundaries = [([0, 0, 0], [20, 20, 20])]
redBoundaries = [([0, 15, 100], [50, 56, 200])]

black = maskcolor(img, blackBoundaries)
red = maskcolor(img, redBoundaries)

kernel = np.ones((5, 5), np.uint8)
red1 = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
red2 = cv2.morphologyEx(red1, cv2.MORPH_OPEN, kernel)
# red1 = cv2.dilate(red, kernel, iterations=1)

#################

redPixels = cv2.findNonZero(red)
x, y, w, h = cv2.boundingRect(redPixels)
# green rectangle
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

rect = cv2.minAreaRect(redPixels)
box = cv2.boxPoints(rect)
box = np.int0(box)
# blue aligned rectangle
cv2.drawContours(img, [box], 0, (255, 0, 0), 2)

p1 = (box[0][0], box[0][1])
p2 = (box[1][0], box[1][1])
p0 = (p2[0], p1[1])

cv2.circle(img, p1, 5, (0, 255, 0), 2)
cv2.circle(img, p2, 5, (0, 255, 0), 2)
cv2.circle(img, p0, 5, (0, 0, 255), 2)

angle2 = math.atan2(p1[1] - p2[1], p1[0] - p2[0])

# img = rotateImage(img, angle2)

#################

cv2.imshow('blackmask', black)
cv2.imshow('redmask', img)

# windowName = 'images'
# cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
# cv2.resizeWindow(windowName, 1600, 450)
# cv2.imshow(windowName, np.hstack([img, np.dstack([mask, mask, mask])]))

cv2.waitKey(0)
cv2.destroyAllWindows()
