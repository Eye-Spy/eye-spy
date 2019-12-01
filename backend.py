
from UserProfile import UserProfile
import os
from WebcamHandler import WebcamHandler

class Backend:
    def gesture_switch(gesture_input):
            switcher = {
                1: 0,
                2: 1,
                3: 2,
                4: 3,
                5: 4,
                6: 5,
                7: 6,
                8: 7,
                9: 8,
                10: 9
            }
            return switcher.get(gesture_input, 11)

    # Get the gesutre and act on it
    def action_On_Gesture(webcam, profile_id) :
        while(True):
            gesture = webcam.get_gesture()
            applicationMapping = UserProfile.get_mapping(profile_id, Backend.gesture_switch(gesture))
            if(applicationMapping != None):
                for each in applicationMapping:
                    os.system("open " + each)