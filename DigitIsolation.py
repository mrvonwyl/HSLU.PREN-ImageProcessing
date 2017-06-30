import numpy as np
import cv2
import copy
import math


class DigitIsolation:
    @staticmethod
    def mask_color(image, boundaries):
        lower = np.array(boundaries[0][0], dtype="uint8")
        upper = np.array(boundaries[0][1], dtype="uint8")
        return cv2.inRange(image, lower, upper)

    #@staticmethod
    #def order_points_roi(pts):



    @staticmethod
    def order_points(pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates as tl, tr, br, bl
        return rect[0], rect[1], rect[2], rect[3]

    @staticmethod
    def four_point_transform(image, pts):

        # obtain a consistent order of the points and unpack them
        # individually
        tr, tl, bl, br = DigitIsolation.order_points(pts)
        rect = np.zeros((4, 2), dtype="float32")
        rect[0] = tl
        rect[1] = tr
        rect[2] = br
        rect[3] = bl

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
            [0, maxHeight - 1]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        # return the warped image
        return warped

    @staticmethod
    def isolate_roman_digit(img):
        black_min = np.array([0, 0, 0], np.uint8)
        black_max = np.array([50, 50, 50], np.uint8)

        # blackBoundaries = [([0, 0, 0], [50, 50, 50])]

        red1_min = np.array([0, 70, 50], np.uint8)
        red1_max = np.array([10, 255, 255], np.uint8)
        red2_min = np.array([170, 70, 50], np.uint8)
        red2_max = np.array([180, 255, 255], np.uint8)

        bgrimg = img
        hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        redmask1 = cv2.inRange(hsvimg, red1_min, red1_max)
        redmask2 = cv2.inRange(hsvimg, red2_min, red2_max)
        redmask = redmask1 | redmask2

        kernel = np.ones((5, 5), np.uint8)
        redmask = cv2.morphologyEx(redmask, cv2.MORPH_CLOSE, kernel)
        redmask = cv2.morphologyEx(redmask, cv2.MORPH_OPEN, kernel)

        imgred = cv2.bitwise_and(bgrimg, bgrimg, mask=redmask)

        cv2.imshow('imgred', imgred)

        # Create a blank 300x300 black image
        height, width = img.shape[:2]
        black = np.zeros((height, width, 3), np.uint8)
        # Fill image with red color(set each pixel to red)
        black[:] = (0, 0, 0)

        #return imgred

        #####################################3

        im2, contours, hierarchy = cv2.findContours(redmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        largeste = 0
        secondlargeste = 0
        largestc = 0
        secondlargestc = 0

        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)

            # eventuell cv2.contourArea(cnt) < 100 verwenden
            if epsilon >= 2:
                if epsilon > largeste:
                    secondlargeste = largeste
                    secondlargestc = largestc
                    largeste = epsilon
                    largestc = cnt

                elif epsilon > secondlargeste:
                    secondlargeste = epsilon
                    secondlargestc = cnt

        if largeste > 0 and secondlargeste > 0:
            rect1 = cv2.minAreaRect(largestc)
            box1 = cv2.boxPoints(rect1)
            box1 = np.int0(box1)

            rect2 = cv2.minAreaRect(secondlargestc)
            box2 = cv2.boxPoints(rect2)
            box2 = np.int0(box2)

            _, tl, bl, _ = DigitIsolation.order_points(box1)
            tr, _, _, br = DigitIsolation.order_points(box2)

            roi = np.zeros((4, 2), dtype="float32")
            roi[0] = tl
            roi[1] = tr
            roi[2] = br
            roi[3] = bl

            cv2.circle(black, (tl[0], tl[1]), 3, (0, 255, 255), 10) # yellow
            cv2.circle(black, (tr[0], tr[1]), 3, (255, 0, 0), 10) # blue
            cv2.circle(black, (br[0], br[1]), 3, (255, 0, 255), 10) # magenta
            cv2.circle(black, (bl[0], bl[1]), 3, (255, 255, 0), 10) # cyan

            cv2.drawContours(black, [box1], 0, (0, 255, 0), 2)
            cv2.drawContours(black, [box2], 0, (0, 255, 0), 2)

        cv2.imshow('roi', black)

        warped = DigitIsolation.four_point_transform(bgrimg, roi)
        blackmask = cv2.inRange(warped, black_min, black_max)
        resized = cv2.resize(blackmask, (800, 450), interpolation=cv2.INTER_CUBIC)

        resized = DigitIsolation.digit_bounding_box(resized)

        return resized


    @staticmethod
    def digit_bounding_box(img):

        cv2.imshow('asd', img)

        margin = 0.18

        black = copy.copy(img)

        kernel = np.ones((5, 5), np.uint8)
        black = cv2.morphologyEx(black, cv2.MORPH_CLOSE, kernel)
        black = cv2.morphologyEx(black, cv2.MORPH_OPEN, kernel)

        _, contours, _ = cv2.findContours(black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        _, iwidth = img.shape[:2]
        width = 0
        height = 0
        y = 0
        h = 0


        for cnt in contours:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w * h > width * height and w > 10 and h > 10:
                width = w
                height = h

        y = math.floor(y + (h * margin))
        h = math.floor(h * (1 - 2 * margin))

        # cv2.rectangle(img, (0, y), (x+iwidth, y+h), (255, 0, 0), 2)

        cv2.imshow('asd', img)

        img = img[y:y+h, 0:iwidth]

        return img
