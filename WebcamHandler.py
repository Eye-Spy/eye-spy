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

# Parameters
threshold = 60
blurValue = 41
bgSubThreshold = 50
learningRate = 0


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

        Thread.__init__(self)
    

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

    def run(self):
        
        webcam = cv2.VideoCapture(0)
        webcam.set(10, 200)
        self.start_time = time.time()

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

                cv2.imshow("New", thresh)
                thresh = cv2.resize(thresh, (125, 125))
                thresh = np.array([thresh.astype('float32')])
                thresh /= 255
                # print(thresh)
                thresh = thresh.reshape((1, 125, 125, 1))

                print(class_dict[np.argmax(self.model.predict(thresh))])

                


    

test = WebcamHandler()
test.start()