import cv2,time

cap = cv2.VideoCapture(0)

#
#time.sleep(2)
#cap.set(11, 5)
#cap.set(8, 1)
#cap.set(14,64)



print("0 CAP_PROP_POS_MSEC  "+ str(cap.get(0)))
print("1 CAP_PROP_POS_FRAMES  "+ str(cap.get(1)))
print("3 CAP_PROP_POS_AVI_RATIO  "+ str(cap.get(3)))
print("4 CAP_PROP_FRAME_WIDTH  "+ str(cap.get(4)))
print("5 CAP_PROP_FRAME_HEIGHT  "+ str(cap.get(5)))
print("6 CAP_PROP_FPS  "+ str(cap.get(6)))
print("7 CAP_PROP_FOURCC  "+ str(cap.get(7)))
print("8 CAP_PROP_FRAME_COUNT  "+ str(cap.get(8)))
print("9 CAP_PROP_FORMAT  "+ str(cap.get(9)))
print("10 CAP_PROP_MODE  "+ str(cap.get(10)))
print("11 CAP_PROP_BRIGHTNESS  "+ str(cap.get(11)))
print("12 CAP_PROP_CONTRAST  "+ str(cap.get(12)))
print("13 CAP_PROP_SATURATION  "+ str(cap.get(13)))
print("14 CAP_PROP_HUE  "+ str(cap.get(14)))
print("15 CAP_PROP_GAIN  "+ str(cap.get(15)))
print("16 CAP_PROP_EXPOSURE  "+ str(cap.get(16)))
print("17 CAP_PROP_CONVERT_RGB  "+ str(cap.get(17)))
print("18 CAP_PROP_RECTIFICATION  "+ str(cap.get(19)))


from pkg_resources import parse_version
OPCV3 = parse_version(cv2.__version__) >= parse_version('3')

# returns OpenCV VideoCapture property id given, e.g., "FPS"
def capPropId(prop):
    return getattr(cv2 if OPCV3 else cv2.cv,
                   ("" if OPCV3 else "CV_") + "CAP_PROP_" + prop)
print (capPropId("FRAME_COUNT"))

while(True):

    #Capture frame-by-frame
    ret, frame = cap.read()
    img = frame
    cv2.imshow("orig", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(.500)