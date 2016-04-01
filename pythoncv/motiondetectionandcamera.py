'''
Reference from: http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
'''

import cv2
import serial
import time

#Grabs camera and sets up serial connection to arduino
camera = cv2.VideoCapture(0)
ser = serial.Serial('/dev/ttyACM0', 9600)

#Sets up working variables
minArea = 1000
frameArea = 10000
firstFrame = None
timeDelay = 500 
degree = 9
currTime = int(round(time.time() * 1000))

try:
    while True:
        (grabbed, rawInput) = camera.read()
        if not grabbed:
            continue
	
	frame = cv2.resize(rawInput, (480, 320)) 
        height, width, channel = frame.shape

        if (frameArea == None):
            frameArea = height*width
            print frameArea

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        #Needs two images to compare
        if firstFrame is None:
            firstFrame = gray
            #time.sleep(0.4)
            continue
        
        #Process the two images and find the differences
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        firstFrame = None
        maxArea = 0
        maxContour = None

        #Finds the biggest difference
        for c in cnts:
            currArea = cv2.contourArea(c)
            if (currArea > minArea) and (currArea < frameArea*0.8):
                if currArea > maxArea:
                    maxArea = currArea
                    maxContour = c
        
        if (maxArea != 0):            
            print maxArea
        

        #Sends a message to the arduino to control camera direction (Needs fine tuning)
        if ((currTime + timeDelay) < int(round(time.time() * 1000))):
            if maxContour != None:
                (x, y, w, h) = cv2.boundingRect(maxContour)
                cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 255, 0), 2)

                x_mid = x + 0.5*w
                y_mid = y + 0.5*h
                message = ""
                if (width/2 > x+w) or (width/2 < x):

                    x_diff = width/2 - x_mid

                    if (x_diff > 0):
                        magnitude = int (abs(x_diff) * degree / (width/2))

                        for i in xrange(magnitude):
                            message = message + "l"
                        print message
                        ser.write(message)
                    else:
                        magnitude = int (abs(x_diff) * degree/(width/2))
                        for i in xrange(magnitude):
                            message = message + "r"
                        print message
                        ser.write(message)

                elif (height/2 > y+h) or (height/2 < y):

                    y_diff = width/2 - y_mid

                    if (y_diff < 0):
                        magnitude = int (abs(y_diff) * degree/(width/2))
                        for i in xrange(magnitude):
                            message = message + "d"
                        print message
                        ser.write(message)
                    elif (y_diff > 0):
                        magnitude = int (abs(y_diff) * degree/(width/2))
                        for i in xrange(magnitude):
                            message = message + "u"
                        print message
                        ser.write(message)
                
                    '''
                    if (x_mid < width/2):
                        ser.write('l')
                    elif (x_mid > width/2):
                        ser.write('r')
                    
                if (height/2 > y+h) or (height/2 < y):
                    if (y_mid > height/2):
                        ser.write('d')
                    elif (y_mid < height/2):
                        ser.write('u')
                    '''
            ser.flush()
            currTime = int(round(time.time() * 1000))                

        
        #Shows images on a window
        cv2.imshow("Input", frame)
        cv2.imshow("Threshold", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()

