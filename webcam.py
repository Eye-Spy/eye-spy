import copy
import cv2
import numpy as np
from tensorflow.keras.models import load_model

LR = 0.1
BGS_THRESH = 50

class WebcamHandler:
	"""
	Manages the operation of the webcame
	"""

	def __init__(self):
		print("Webcam init")

		self.bgModel = cv2.createBackgroundSubtractorMOG2(0, BGS_THRESH)
	
	def segment(self, image, threshold=25):

		global bg

		diff = cv2.absdiff(bg.astype("uint8"), image)

		(_, contours, _ ) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# No hand detected
		if len(contours) == 0:
			return 
		else:

			segmented = max(contours, key=cv2.contourArea)
			return (threshold, segmented)

	def remove_background(self, frame):
		"""
		Uses OpenCV's built in background subtractor to extreact the 
		foreground by removing the background
		"""
		foreground_mask = self.bgModel.apply(frame, learningRate=LR)
		kernel = np.ones((3,3), np.uint8)
		foreground_mask = cv2.erode(foreground_mask, kernel, iterations=1)
		result = cv2.bitwise_and(frame, frame, mask=foreground_mask)

		return result


	def run_webcam(self):

		camera = cv2.VideoCapture(0)
		while(True):


			(grabbed,frame) = camera.read()
			cv2.imshow("Feed", frame)

			if cv2.waitKey(1) == 27:
				break

test = WebcamHandler()
test.run_webcam()