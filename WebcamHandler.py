from threading import Thread

import tensorflow.keras as keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import categorical_crossentropy

import cv2

class WebcamHandler(Thread):

    def __init__(self):
        print("Works")
        self.model = self.build_gesture_model()

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

    def run(self):

        while (True):
            webcam = cv2.VideoCapture(0)
test = WebcamHandler()
test.start()
