import cv2

class VideoCamera(object):

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        self.video = cv2.VideoCapture(0)
        self.minArea = 1000 

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
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
