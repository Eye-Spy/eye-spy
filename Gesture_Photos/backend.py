import UserProfile
import gui
import subprocess

# Get the profile
# This is just a place holder for now until
# the actual function is written to obtain
# the profile from the gui

#def get_Profile() :
    #profile = gui.get_profile()

def gesture_switch(gesture_input):
        switcher = {
            0: "noise",
            1: "one_finger",
            2: "two_finger",
            3: "three_finger",
            4: "four_finger",
            5: "five_finger",
            6: "fist",
            7: "thumbs_up",
            8: "thumbs_down",
            9: "okay",
            10: "c_hand"
        }
        return switcher.get(gesture_input, "noise")

# Get the gesutre and act on it
def action_On_Gesture() :
    while webcam.is_read() == True  :
        gesture = WebcamHandler.webcam.get_gesture()
        applicationMapping = get_mapping(profile, gesture_switch(gesture) )
        subprocess.run(applicationMapping)


# Driver program 
if __name__ == "__main__": 
	argument=2
 	test = gesture_switch(argument)
print(test)