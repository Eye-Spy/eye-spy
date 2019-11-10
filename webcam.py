import copy
import cv2
import numpy as np
import imutils
import traceback
from tensorflow.keras.models import load_model



LR = 0.001
BGS_THRESH = 50


AVG_WEIGHT = 0.5
class WebcamHandler:
	"""
	Manages the operation of the webcame
	"""

	def __init__(self):
		print("Webcam init")

		self.bgModel = cv2.createBackgroundSubtractorMOG2(0, BGS_THRESH)
		self.hand_model = cv2.CascadeClassifier('aGest.xml')
		self.ready_frames = 0

		self.top, self.right, self.bottom, self.left = 10, 350, 225, 590

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
	def get_greyscale(self):

		(grabbed, frame) = self.webcam.read()
		frame = imutils.resize(frame, width=700)
		frame = cv2.flip(frame, 1)

		clone = frame.copy()

		(height, width) = frame.shape[:2]
		#region_of_interest = frame[self.top:self.bottom, self.right:self.left]
		region_of_interest = frame


		gray = cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7,7), 0)

		return gray, clone
	
	def set_background(self):
		"""
		Grabs 30 frames from the camera and uses them to 
		set the background image
		"""

		# Grab the global background 
		global bg

		image, _ = self.get_greyscale()
		
		# Resets the global background to the image in front
		# of the screen
		bg = image.copy().astype("float")
		for i in range(30):
			image, _ = self.get_greyscale()
			# cv2.imshow("test", image)
			cv2.accumulateWeighted(image, bg, AVG_WEIGHT)
	


	def find_hand(self):
		try:
			ret, frame = self.webcam.read()
			frame = cv2.flip(frame, 1)
			kernel = np.ones((3,3), np.uint8)

			region_of_interest = frame[100:300, 100:300]
			#region_of_interest = frame

			cv2.rectangle(frame, (100,100), (300,300), (0, 255, 0), 0)
			hsv = cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2HSV)

			skin_l = np.array([0, 20, 70], dtype=np.uint8)
			skin_h = np.array([20, 255, 255], dtype=np.uint8)

			msk = cv2.inRange(hsv, skin_l, skin_h)

			msk = cv2.dilate(msk, kernel, iterations= 4)

			msk = cv2.GaussianBlur(msk, (5, 5), 100)

			cnt, hier = cv2.findContours(msk, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			
			cnt = max(cnt, key = lambda x: cv2.contourArea(x))
			eps = 0.0005*cv2.arcLength(cnt, True)
			apx = cv2.approxPolyDP(cnt, eps, True)
			
			hull = cv2.convexHull(cnt)

			ahull = cv2.contourArea(hull)
			areacount = cv2.contourArea(cnt)
			areart = ((ahull - areacount)/ areacount) * 100

			hull = cv2.convexHull(apx, returnPoints=False)
			defects = cv2.convexityDefects(apx, hull)

			cv2.imwrite("test.png", frame)
		except Exception as e:
			print("Failed: ", e)

			print(''.join(traceback.format_tb(e.__traceback__)))
			exit(0)
			return None


	def start_webcam(self):
		self.webcam = cv2.VideoCapture(0)


	def main_loop(self):

		while(1):
			test = self.find_hand()
		

test = WebcamHandler()
test.start_webcam()
test.main_loop()
