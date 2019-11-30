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


class WebcamHandler(Thread):

    def __init__(self, show_box = False):
        print("Works")
        self.model = self.build_gesture_model()
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
        self.close_flag = True
        return

    def build_gesture_model(self):
        
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

        fgmask = bgModel.apply(frame, learningRate=learningRate)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res

    def capture_background(self):

        time.sleep(1)
        self.bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        self.isBackgroundCaptured = 1
        self.system_ready = True
    
        print("Background Captured")
        time.sleep(1)
    
    def reset_detection(self):
        """
        Utility for forgetting currently selected gesture
        """

        self.imm_conf = 0
        self.last_read = 0

    def get_gesture(self):
        return self.current_gesture()
    
    def is_ready(self):
        return self.system_ready

    def run(self):
        
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
                img = self.remove_background(frame, self.bgModel)
                img = img[0:int(500), int(frame.shape[1] - 500):frame.shape[1]]
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
                #cv2.imshow('blur', blur)
                ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

                #cv2.imshow("New", thresh)
                self.cur_image = thresh
                thresh = cv2.resize(thresh, (125, 125))
                thresh = np.array([thresh.astype('float32')])
                thresh /= 255
                # print(thresh)
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
                
                if self.close_flag:
                    webcam.release()
                    self.is_ready = False
                    return

# For testing purposes 
if __name__ == "__main__":
    test = WebcamHandler()
    test.start()
    while(1):
        try:
            image = test.cur_image
            cv2.imshow("test", image)
        except:
            pass
