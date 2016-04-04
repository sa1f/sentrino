import cv2
import numpy

#Initialize the camera
camera = cv2.VideoCapture(0)

#Color threshold definitions
redLow_HSV = numpy.array([0, 150, 122])
redHigh_HSV = numpy.array([57, 255, 255])
greenLow_HSV = numpy.array([57,131,0])
greenHigh_HSV = numpy.array([101, 255, 255])

#Minimum contour area
minArea = 5000

#Calibration Variables
calibration = False
h_low = 0
h_high = 0
s_low = 0
s_high = 179
v_low = 255
v_high = 255


def updateValues(x):
    pass

#Calibration Window creation
if calibration: 
    cv2.namedWindow("Calibration")
    cv2.createTrackbar("H_l", "Calibration", 0, 179, updateValues)
    cv2.createTrackbar("S_l", "Calibration", 0 ,255, updateValues)
    cv2.createTrackbar("V_l", "Calibration", 0 ,255, updateValues)
    cv2.createTrackbar("H_h", "Calibration", 0, 179, updateValues)
    cv2.createTrackbar("S_h", "Calibration", 0 ,255, updateValues)
    cv2.createTrackbar("V_h", "Calibration", 0 ,255, updateValues)





try:
    while True:

        #Gets image from camera
        (grabbed, frame) = camera.read()
        if not grabbed:
            break
        
        #Converts to HSV colorspace
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #Updates values if calibrating
        if calibration:
            h_low = cv2.getTrackbarPos("H_l", "Calibration")
            h_high = cv2.getTrackbarPos("H_h", "Calibration")
            s_low = cv2.getTrackbarPos("S_l", "Calibration")
            s_high = cv2.getTrackbarPos("S_h", "Calibration")
            v_low = cv2.getTrackbarPos("V_l", "Calibration")
            v_high = cv2.getTrackbarPos("V_h", "Calibration")
            low = numpy.array([h_low, s_low, v_low])
            high = numpy.array([h_high, s_high, v_high])
            mask = cv2.inRange(hsv, low, high)

        #Red and Green filtered to binary images
        redBinary = cv2.inRange(hsv, redLow_HSV, redHigh_HSV)
        greenBinary = cv2.inRange(hsv, greenLow_HSV, greenHigh_HSV)

        #Contours found
        (redCnts, _) = cv2.findContours(redBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (greenCnts, _) = cv2.findContours(greenBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        maxArea = 0
        maxRedContour = None

        #Finds the maximum in contours
        for c in redCnts:
            currArea = cv2.contourArea(c)
            if currArea > minArea:
                maxArea = currArea
                maxRedContour = c
        if maxArea != 0:
            print maxArea

        maxGreenContour = None
        maxArea = 0

        for c in greenCnts:
            currArea = cv2.contourArea(c)
            if currArea > minArea:
                maxArea = currArea
                maxGreenContour = c
        if maxArea != 0:
            print maxArea

        height, width, channels = frame.shape

        if maxRedContour != None:
            (x, y, w, h) = cv2.boundingRect(maxRedContour)
            cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 0, 255), 2)

        if maxGreenContour != None:
            (x, y, w, h) = cv2.boundingRect(maxGreenContour)
            cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 255, 0), 2)

        if maxRedContour != None:
            cv2.putText(frame, "ENEMY ALERT", (0, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
        elif maxGreenContour != None:
            cv2.putText(frame, "HELLO FRIEND", (0, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0))

        #(cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.imshow("hsv", hsv)
        cv2.imshow("input", frame)
        #cv2.imshow("mask", mask)

       
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()

'''
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, redLow_HSV, redHigh_HSV)
RED: 
133-179
105-255
94-255
---------
0-42
150-255
122-255

GREEN:
57-101
131-255
0-255
'''