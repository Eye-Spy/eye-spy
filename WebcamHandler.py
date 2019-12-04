import time
import numpy as np

from threading import Thread

import tensorflow.keras as keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import categorical_crossentropy

import cv2

from backend import Backend

# Parameters for vision
threshold = 60
blurValue = 41
bgSubThreshold = 50
learningRate = 0

CONFIDENCE_REQ = 20

class_dict = {
    0 : "noise",
    1 : "one_finger",
    2 : "two_fingers",
    3 : "three_fingers",
    4 : "four_fingers",
    5 : "five_fingers",
    6 : "fist",
    7 : "thumbs_up",
    8 : "thumbs_down",
    9 : "okay",
    10: "c_hand"
}

"""
Thread object for handleing all Webcam functions.
"""
class WebcamHandler(Thread):

    def __init__(self, profile = None, show_box = False):
        print("Works")
        self.model = self.build_gesture_model()
        self.profile = profile
        self.isBackgroundCaptured = 0
        self.current_gesture = 0
        self.show_box = show_box
        self.system_ready = False
        self.cur_image = None 
        self.close_flag = False

        # Represnts the length at which the current gesture has been in
        # front of the screen and what that gesture has been
        self.imm_conf = 0
        self.last_read = 0

        Thread.__init__(self)
    def close(self):
        """
        Ends the Webcam Thread

        Raises a flag which causes the run function of the thread
        to cease looping, allowing the main thread to successfully
        join the webcam thread

        Parameteres:
        None

        Returns:
        None

        """
        self.close_flag = True
        return

    def build_gesture_model(self):
        """
        Builds the Nueral Network for gesture recognition

        Builds a network with a combination of convolutional layers
        and dense layers for the purpose of recgonizing gestures, then 
        loads in the pre-trained weights.

        Parameters:
        None

        Returns:
        Keras Sequential Model: Pre-trained nueral network to recognize 
                                gestures.
        """
        
        num_classes = 11
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(5, 5),
                 activation='relu',
                 input_shape=(125, 125, 1)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))

        model.compile(loss=categorical_crossentropy,
              optimizer=Adam(),
              metrics=['accuracy'])
        
        model.load_weights('GestureModel.h5')

        return model
    
    def remove_background(self, frame, bgModel):
        """
        Removes the background of a frame

        Uses the trained background subtractor to eliminate anything in
        the given frame not present in the original background reference
        created when Eye Spy was launched. Once that foreground mask is 
        created, a black and white filter is applied to the frame and 
        it is returned.

        Parameters:
        frame (np.ndarray) Array representing the frame
        bgModel: OpenCV model created to subtract the background

        Returns:
        res: Frame with background removed        
        """

        fgmask = bgModel.apply(frame, learningRate=learningRate)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res

    def capture_background(self):
        """
        Captures the background as a reference

        Uses OpenCV's background subtraction method to create a 
        reusable model for subtracting the background from an
        image. Indicates that the system is ready to accept gestures
        once finished.

        Parameters:
        None

        Returns:
        None
        """

        time.sleep(1)
        self.bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        self.isBackgroundCaptured = 1
        self.system_ready = True
    
        print("Background Captured")
        time.sleep(1)
    
    def reset_detection(self):
        """
        Resets the detection confidence

        Parameters:
        None

        Returns:
        None
        """

        self.imm_conf = 0
        self.last_read = 0

    def get_gesture(self):
        """
        Getter for the most recently processed frame

        Parameters:
        None

        Returns:
        self.current_gesture (np.ndarray): numpy array representing
                                           the most recent image 
        """
        return self.current_gesture
    
    def is_ready(self):
        """
        Getter for if the system is ready

        Will always return false until the background has 
        been fully obtained and processed.

        Parameters:
        None

        Returns:
        self.system_ready (Bool): Boolean representing if the system is
                                  ready or not.
        """
        return self.system_ready

    def run(self):
        """
        Main loop function for Webcam Thread

        Begins by opening the webcam and reducing the frame down to
        the top right and corner of the camera. Starts by capturing the 
        background and waiting for a few seconds to allow the system to 
        catch up. Then, it will continuely process frames and predict for 
        gestures until an interrupt signal is recieved  (via close). If 
        it detects the same gesture 20 times in a row, it will query the 
        backend for the relevent gesture.

        Parameters:
        None

        Returns:
        None
        """
        
        webcam = cv2.VideoCapture(0)
        webcam.set(10, 200)
        self.start_time = time.time()
        self.close_flag = False

        while webcam.isOpened():
            
            k = cv2.waitKey(10)
            if (not self.system_ready) and (time.time() - self.start_time >= 3):
                self.capture_background()
            
            ret, frame = webcam.read()

            frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
            frame = cv2.flip(frame, 1)  # flip the frame horizontally
            cv2.rectangle(frame, (int(frame.shape[1] - 500), 0),
                        (frame.shape[1], 500), (255, 0, 0), 2)
            #cv2.imshow('original', frame)
            if self.isBackgroundCaptured == 1:

                # Removes the background from the image
                img = self.remove_background(frame, self.bgModel)
                img = img[0:int(500), int(frame.shape[1] - 500):frame.shape[1]]
                
                # Applies blur and black and white filter
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
                ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

                #cv2.imshow("New", thresh)
                self.cur_image = thresh

                # Shrinks the image to be read by the nueral network
                thresh = cv2.resize(thresh, (125, 125))
                thresh = np.array([thresh.astype('float32')])
                thresh /= 255
                thresh = thresh.reshape((1, 125, 125, 1))

                cur = np.argmax(self.model.predict(thresh))

                if cur != self.last_read or cur == 0:
                    self.imm_conf = 0
                    self.last_read = cur
                else:
                    self.imm_conf += 1

                    # If the length at which the current gesture has been read is sufficient
                    # we set it has the currently detected gesture 
                    if self.imm_conf / CONFIDENCE_REQ >= 1:
                        self.current_gesture = cur
                        print("Detected", class_dict[self.current_gesture], "!")
                        Backend.action_On_Gesture(self, self.profile)
                        self.imm_conf = 0
                # Checks to see if the thread is ready to close
                if self.close_flag:
                    webcam.release()
                    self.is_ready = False
                    return

# For testing purposes 
if __name__ == "__main__":
    test = WebcamHandler()
    test.start()
