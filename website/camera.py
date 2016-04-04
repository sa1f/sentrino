import cv2
import numpy
import requests
import time


class VideoCamera(object):

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        
        #The camera capturing object
        self.video = cv2.VideoCapture(0)

        #Color Detection Constants
        self.minArea = 1000
        self.redLow_HSV = numpy.array([0, 150, 122])
        self.redHigh_HSV = numpy.array([57, 255, 255])
        self.greenLow_HSV = numpy.array([57,131,0])
        self.greenHigh_HSV = numpy.array([101, 255, 255])
        
        #Enemy Recording Variables
        self.enemyDetected = False
        self.enemyOnScreenTime = 2000
        self.record = False
        self.enemyTimeTracker = None
        self.recorder = None
        self.enemyLastSeen = 0
        
    def __del__(self):
        self.video.release()

    @staticmethod
    def millis():
        return int(round(time.time() * 1000))
    
    def get_frame(self):

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        while True:
            (grabbed, frame) = self.video.read()
            if grabbed:
                break            

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Filter the binary images for each color
        redBinary = cv2.inRange(hsv, self.redLow_HSV, self.redHigh_HSV)
        redBinary = cv2.GaussianBlur(redBinary, (21,21), 0)

        greenBinary = cv2.inRange(hsv, self.greenLow_HSV, self.greenHigh_HSV)
        greenBinary = cv2.GaussianBlur(greenBinary, (21,21), 0)

        #Find the contours, i.e. objects and indentify them
        (redCnts, _) = cv2.findContours(redBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (greenCnts, _) = cv2.findContours(greenBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        maxArea = 0
        maxRedContour = None

        #Finds the largest Red object
        for c in redCnts:
            currArea = cv2.contourArea(c)
            if currArea > self.minArea:
                maxArea = currArea
                maxRedContour = c
        '''
        if maxArea != 0:
            print maxArea
        '''

        #Find the largest green object
        maxGreenContour = None
        maxArea = 0

        for c in greenCnts:
            currArea = cv2.contourArea(c)
            if currArea > self.minArea:
                maxArea = currArea
                maxGreenContour = c
        '''
        if maxArea != 0:
            print maxArea
        '''

        #Image dimensions
        height, width, channels = frame.shape


        #Make rectangles on the image
        if maxGreenContour != None:
            (x, y, w, h) = cv2.boundingRect(maxGreenContour)
            cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 255, 0), 2)

        if maxRedContour != None:
            if (self.enemyDetected):
                if ((self.enemyTimeTracker + self.enemyOnScreenTime) < self.millis()) and not self.record:
                    print "Starting Record"
                    self.record = True
            else:
                self.enemyDetected = True
                self.enemyTimeTracker = self.millis()
            
            (x, y, w, h) = cv2.boundingRect(maxRedContour)
            cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 0, 255), 2)

            '''
            #Send alert of an enemy
            print requests.get('http://localhost:5000/alert/enemy')
            
            x_mid = x + 0.5*w
            y_mid = y + 0.5*h

            #Moves camera left or right
            if (width/2 > x+w) or (width/2 < x):

                if (x_mid < width/2):
                    print requests.get('http://localhost:5001/automove/left')
                elif (x_mid > width/2):
                    print requests.get('http://localhost:5001/automove/right')
            
            #Moves camera up or down
            if (height/2 > y+h) or (height/2 < y):
                if (y_mid > height/2):
                    print requests.get('http://localhost:5001/automove/down')
                elif (y_mid < height/2):
                    print requests.get('http://localhost:5001/automove/up')
            '''
            self.enemyLastSeen = self.millis()
        else:
            if (self.enemyLastSeen + self.enemyOnScreenTime < self.millis()):
                self.enemyDetected = False
                self.record = False


        #Text
        if maxRedContour != None:
            cv2.putText(frame, "ENEMY", (0, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 10)
        
        elif maxGreenContour != None:
            cv2.putText(frame, "FRIEND", (0, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 10)

        if (self.record):
            if (self.recorder == None):
                print "Initialized recorder"
                
                filename = 'saved/' + time.strftime("%Y-%b-%d-%H_%M_%S.avi", time.localtime())

                print "File saved as: " + filename

                self.recorder = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC(*'XVID'), 5, (width, height))
            print "Recording"
            self.recorder.write(frame)
        else:
            if (self.recorder != None):
                print "Finished"
                self.recorder.release()
                self.recorder = None

        image = cv2.resize(frame, (100, 67))
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()



















        '''
        BELOW CODE FOR MOTION DETECTION (IMPERFECT)
        differenceSet = False
        firstFrame = None
        frame = None
        while not differenceSet:
            (grabbed, frame) = self.video.read()
            if not grabbed:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if firstFrame is None:
                firstFrame = gray
                continue

            differenceSet = True
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations = 2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            firstFrame = None
            maxArea = 0
            maxContour = None
            for c in cnts:
                currArea = cv2.contourArea(c)
                if currArea > self.minArea:
                    if currArea > maxArea:
                        maxArea = currArea
                        maxContour = c
                        #print currArea
    
            if maxContour != None:
                (x, y, w, h) = cv2.boundingRect(maxContour)
                cv2.rectangle(frame, (x, y), (x + w, y +  h), (0, 255, 0), 2)

                
        image = cv2.resize(frame, (100, 67))
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()
        '''
