import numpy as np
import cv2,math

cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # find only red colors in video stream
    lower = np.array([40, 10,170], dtype="uint8")
    upper = np.array([100, 100, 200], dtype="uint8")
    mask = cv2.inRange(frame,lower,upper)
    output = cv2.bitwise_and(frame, frame, mask = mask)

    #OutputFile weiter analysieren
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    minLineLength=gray.shape[1]-300
    lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi/500, threshold=10, lines=np.array([]),
                            minLineLength=50, maxLineGap=100)

    # Nur etwas machen, wenn mindestens 1 Linie entedeckt wurde
    if lines is not None:
        a,b,c = lines.shape
        for i in range(a):
            print("X1:",(lines[i][0][0]," -- y1:", lines[i][0][1])," -- x2:", (lines[i][0][2]," -- y2:", lines[i][0][3]))
            # Berechnung des Winkels jeder Linie

            angle = int(math.atan((lines[i][0][1]-lines[i][0][3])/(lines[i][0][2]-lines[i][0][0]))*180/math.pi)
            print(angle)

            # Nur die Linien ausgeben, welche wahrscheinlich Horizontal sind
            if(angle>45 or angle<-45):
                cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (255, 0, 0), 3,
                         cv2.LINE_AA)

    # show the images
    cv2.imshow("images", np.hstack([frame, output]))
    cv2.imshow("edges", np.hstack([edges, gray]))
    #cv2.waitKey(0);


    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()