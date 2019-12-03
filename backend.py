from UserProfile import UserProfile
import os
import time 

class Backend:
    def gesture_switch(gesture_input):
        """
        Takes the gesture_input from the webcam and passes the correct Gesture ID to the
        action_On_Gesture function

        Takes gesture_input and returns the correct gesture id

        Parameters:
        gesture_input: an integer representing the gesture identified by the neural network

        Returns:
        The adjusted gesture identifier integer to access the appropriate config.json mappings
        """
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
        """
        Executes the application mappings for the selected User Profile based on the gesture identified by the webcam

        Uses get_mapping on the selected profile_id and identified gesture to retrieve the application mappings list,
        then executes each mapping

        Parameters:
        webcam: a reference to the currently running WebcamHandler object
        profile_id: the currently selected profile_id

        Returns:
        None
        """
        gesture = webcam.get_gesture()
        applicationMapping = UserProfile.get_mapping(profile_id, Backend.gesture_switch(gesture))
        if(applicationMapping != None):
            for each in applicationMapping:
                os.system("open " + each)