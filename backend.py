sample = 2

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
	argument=0
	test = gesture_switch(argument) 
    
print(test)