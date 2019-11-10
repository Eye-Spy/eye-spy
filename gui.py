from tkinter import *
import platform

class Systemcall:
    def init(calls, os):
        calls.os = platform.system()

class UserProfile:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

class gestures:
    def __intit__(gesture, name, images):
        gesture.name = name
        gestrureimg = PhotoImage(file = name)
    def display():
        label = Label(op, image = gestureimg)
        label.pack()

win = Tk()
topFrame = Frame(win)
topFrame.pack()
bottomFrame = Frame(win)
bottomFrame.pack(side=BOTTOM)

def doNothing():
   print("this function does nothing")


def createNew():
    def openGesture():
        options = [
            "gesture 1",
            "gesture 2",
            "gesture 3",
            "gesture 4",
            "gesture 5",
            "gesture 6",
            "gesture 7",
            "gesture 8",
            "gesture 9",
            "gesture 10",
            "gesture 11",
        ]
        clicked = StringVar()
        clicked.set(options[0])
        dropg = OptionMenu(op,clicked,*options)
        dropg.pack(side=LEFT)
        
        okayg = Button(op,text="okay",command = openmappings)
        okayg.pack(side=LEFT)
    def adder():
        userinput = Toplevel(op)
        name = Label(userinput,text = "Please enter application name")
        name.pack()
        ent = Entry(userinput)
        ent.pack()
        search = Button(userinput,text="Search applications",command = doNothing)
        search.pack()
    def openmappings():
        add = Button(op,text = "add application",command = adder)
        add.pack(side=RIGHT)
        options =[
            "Mapping 1",
            "Mapping 2",
            "Mapping 3"
            ]
        clicker = StringVar()
        clicker.set("Mappings")
        dropm = OptionMenu(op,clicker,*options)
        dropm.pack(side=RIGHT)
    op = Toplevel(win)
    op.configure(background='grey')
    topFrame = Frame(op)
    topFrame.pack()
    bFrame = Frame(op)
    bFrame.pack(side = BOTTOM)

    name = Label(topFrame,text = "EYE SPY",bg='grey')
    name.pack(side=LEFT)

    var = StringVar()
    var.set("Please select user profile")
    drop = OptionMenu(op, var, "UserPofile1","UserProfile2","UserProfile3")
    drop.pack(side=LEFT)

    okay = Button(op,text="Okay",command = openGesture)
    okay.pack(side=LEFT)

    beginspy = Button(bFrame, text="Begin Eye Spy", bg= 'black',fg = 'yellow')
    beginspy.pack(side=LEFT)


win.title("Eye Spy")
win.configure(background= 'grey')
banner = PhotoImage(file="Eye spy.png")

B = Button(bottomFrame, image = banner, command = createNew)
B.pack()



win.mainloop()

