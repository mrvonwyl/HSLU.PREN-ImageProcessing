import numpy as np
import cv2


def mask_color(image, boundaries):
    lower = np.array(boundaries[0][0], dtype="uint8")
    upper = np.array(boundaries[0][1], dtype="uint8")
    return cv2.inRange(image, lower, upper)


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def isolate_roman_digit(img):
    black_boundaries= [([0, 0, 0], [50, 50, 50])]
    red_boundaries = [([0, 15, 100], [70, 70, 210])]

    black = mask_color(img, black_boundaries)
    red = mask_color(img, red_boundaries)

    kernel = np.ones((5, 5), np.uint8)
    red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
    red = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel)

    cv2.imshow("redMask", red)

    im2, contours, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    i = 0
    rect = np.zeros((4, 2), dtype = "float32")

    for cnt in contours:
        epsilon = 0.01 * cv2.arcLength(cnt, True)

        print(epsilon)

        if epsilon >= 2:
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            pts = np.array([tuple(approx[0][0]), tuple(approx[1][0]), tuple(approx[2][0]), tuple(approx[3][0])], dtype = "float32")
            pts = order_points(pts)

            if i == 0:
                rect[0] = pts[1]
                rect[1] = pts[2]

                cv2.rectangle(img, (10, 10), (30, 30), (0, 255, 0), 2)
            elif i == 1:
                rect[2] = pts[0]
                rect[3] = pts[3]

            i += 1

    warped = four_point_transform(black, rect)
    resized = cv2.resize(warped, (800, 450), interpolation=cv2.INTER_CUBIC)
    return resized
