import cv2


camera = cv2.VideoCapture(0)

try:
	while True:
		(grabbed, frame) = camera.read()
		if not grabbed:
			break
		
		cv2.imshow("Input", frame)

finally:
	camera.release()
	cv2.destroyAllWindows()
