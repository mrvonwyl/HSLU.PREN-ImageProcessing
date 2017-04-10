import time

import cv2
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
    edges = cv2.Canny(resized,50,150,apertureSize = 3)
    #lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
    #lines = cv2.HoughLinesP(image=edges,rho=0.1,theta=np.pi/500, threshold=19,lines=np.array([]), minLineLength=100,maxLineGap=100)
    lines = cv2.HoughLinesP(image=edges,rho=2,theta=np.pi/180, threshold=130,lines=np.array([]), minLineLength=120,maxLineGap=100)
    print("Anzahl Linien:")
    print(len(lines))
    draw_im = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    for line in lines:
        x1,y1,x2,y2 = line[0]
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
