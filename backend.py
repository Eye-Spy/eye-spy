import WebcamHandler


def profile1():
    return "profile1"

def profile2():
    return "profile2"

def profile3():
    return "profile3"

def profile4():
    return "profile4"

def profile5():
    return "profile5"

def profile6():
    return "profile6"

def profile7():
    return "profile7"

def profile8():
    return "profile8"

def profile9():
    return "profile9"

def profile10():
    return "profile10"




#Get the Gesture

WebcamHandler.webcam.get_gesture()







def gesture_switch(sample):
        switcher = {
            1: "test",
            2: "basic",
            3: "switch",
            4: "statment"
        }
        return switcher.get(sample, "Wrong Answer laddy")

# Driver program 
if __name__ == "__main__": 
	argument=2
	test = gesture_switch(argument) 
    
print(test)