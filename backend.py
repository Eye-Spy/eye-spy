#import WebcamHandler
import UserProfile

#Get the gesutre
#gesture = WebcamHandler.webcam.get_gesture()


def gesture_switch(gesture_input):
        switcher = {
            0: "nothing",
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
        return switcher.get(gesture_input, "Wrong Answer laddy")


def profile1():
    get_mapping(1, gesture_switch(gesture) )
    return "profile1"

def profile2():
    get_mapping(2, gesture_switch(gesture) )
    return "profile2"

def profile3():
    get_mapping(3, gesture_switch(gesture) )
    return "profile3"

def profile4():
    get_mapping(4, gesture_switch(gesture) )
    return "profile4"

def profile5():
    get_mapping(5, gesture_switch(gesture) )
    return "profile5"

def profile6():
    get_mapping(6, gesture_switch(gesture) )
    return "profile6"

def profile7():
    get_mapping(7, gesture_switch(gesture) )
    return "profile7"

def profile8():
    get_mapping(8, gesture_switch(gesture) )
    return "profile8"

def profile9():
    get_mapping(9, gesture_switch(gesture) )
    return "profile9"

def profile10():
    get_mapping(10, gesture_switch(gesture) )
    return "profile10"


# Driver program 
if __name__ == "__main__": 
	argument=2
	test = gesture_switch(argument)

print(test)