import time

import cv2, math
import numpy as np

from DigitIsolation import DigitIsolation

img = cv2.imread('images/Nr4.png')

cap = cv2.VideoCapture('images/v2.webm')
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # img = frame
    cv2.imshow("orig", img)
    resized = DigitIsolation.isolate_roman_digit(img)
    cv2.imshow('resized', resized)

    # Nur Konturen einzeichnen
    th, bw = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    edges = cv2.Canny(resized, th/2, th)
    cv2.imshow('edges', edges)

    #Draw_im = farbiges Bild, damit man erkennte linien auch sieht.
    draw_im = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)

    #Linien finden.  Und rot einzeichnen
    lines = cv2.HoughLinesP(image=edges,rho=2,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=200,maxLineGap=30)
    draw_im = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(draw_im,(x1,y1),(x2,y2),(0,0,255),1)
    cv2.imshow('draw_im', draw_im)

    #Mit Rot eingezeichneten Linien weiterarbeiten
    # Irgendwie will ich hier versuchen, die linien zu Gruppieren
    red_boundaries = [([0, 0, 250], [0, 0, 255])]
    lower = np.array(red_boundaries[0][0], dtype="uint8")
    upper = np.array(red_boundaries[0][1], dtype="uint8")
    red= cv2.inRange(draw_im, lower, upper)
    cv2.imshow('red', red)

    # Neu mit den nur Roten Linien weiterarbeiten. So habe ich schöne Geraden und könnte diese weiterverwenden
    kernel = np.ones((4,4), np.uint8)
    kernel_5x5 = np.ones((5,5), np.float32) / 5.0
    output = cv2.filter2D(red, -1, kernel_5x5)
    cv2.imshow('output', output)
    img_erosion = cv2.erode(output, kernel, iterations=1)
    cv2.imshow('img_erosion', img_erosion)

    height, width = img_erosion.shape[:2]
    print(height)
    lines = cv2.HoughLinesP(image=img_erosion,rho=2,theta=np.pi/180, threshold=200,lines=np.array([]), minLineLength=200,maxLineGap=30)
    print("Anzahl Linien:")
    print(len(lines))
    draw_im = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    for line in lines:
        x1,y1,x2,y2 = line[0]

        deltaX=x2-x1
        deltaY=y2-y1
        temp=(deltaX*deltaX)+(deltaY*deltaY)
        length=math.sqrt(temp)
        print(length)

        #print("x1: "+str(x1)+" x2: "+str(x2))
        # print("y1: "+str(y1)+" y2: "+str(y2))
        #if((x2)<(x1-(x1*0.2))) or ((x2)<(x1+(x1*0.2))):
        #print("nicht")
        #else:
        #print("gerade")
        cv2.line(draw_im,(x1,y1),(x2,y2),(0,0,255),2)
    print ("---")
    cv2.imshow('draw_im', draw_im)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
