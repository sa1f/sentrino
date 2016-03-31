import cv2
import serial


camera = cv2.VideoCapture(0)
ser = serial.Serial('dev/ttyACM0', 9600)
minArea = 5000
firstFrame = None 

try:
    while True:
        (grabbed, frame) = camera.read()
        if not grabbed:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue
        
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        firstFrame = None
        maxArea = 0
        maxContour = None
        for c in cnts:
            currArea = cv2.contourArea(c)
            if currArea > minArea:
                if currArea > maxArea:
                    maxArea = currArea
                    maxContour = c
                    print currArea
        
        if maxContour != None:
            (x, y, w, h) = cv2.boundingRect(maxContour)
            cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 255, 0), 2)

        cv2.imshow("Input", frame)
        cv2.imshow("Threshold", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()

