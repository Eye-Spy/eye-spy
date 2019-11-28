
from tkinter import *
import platform
from tkinter import ttk
from tkinter import filedialog

class Systemcall:
    def __init__(self,os):
        calls.os = platform.system()
class UserProfiles:
    def __init__(self):
        return
    # creates a name for the user and links it to the name that was clicked. 
    # Also creates gesture list box and populates it with the gesture names.
    def create_new(self,name):
        self.name = name
        GUI.CreateListBoxG(self)
        self.options = [
            "one_finger",
            "two_finger",
            "three_finger",
            "four_finger",
            "five_finger",
            "fist",
            "thumbs_up",
            "thumbs_down",
            "okay",
            "c_hand",
            "-",
        ]
        self.allG = StringVar()
        for each in self.options:
            self.listboxG.insert(END,each)
        #print(self.name)
        
    #doest do anything yet   
    def add_mapping(self):
        return
    #doesnt do anything yet
    def remove_mapping(self):
        return
    #creates a listbox for the mappings 
    def get_mapping(self,gesture):
        self.gesture=gesture
        GUI.CreateListBoxM(self)
        
class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Eye Spy")
        master.configure(background = 'grey')
        self.banner = PhotoImage(file="Eye spy.png")
        self.B = Button(master,image = self.banner, command = self.openNew)
        self.B.pack()

    # opens the operational window and calls the begin eye spy button function and creates the list box for user profiles    
    def openNew(self):
        self.OW = Toplevel(self.master)
        self.OW.configure(background='grey')
        self.tFrame = Frame(self.OW)
        self.tFrame.pack()
        self.bFrame = Frame(self.OW)
        self.bFrame.pack(side=BOTTOM)
        self.logo = PhotoImage(file="smaller logo 2.png")
        self.picture = Label(self.OW,image= self.logo)
        self.picture.pack(side=TOP,expand ="yes")

        self.beginEyeButton()
        self.CreateListBox()

    def beginEyeButton(self):
        self.beginspy = Button(self.bFrame, text = "Begin Eye Spy",bg ='black',fg='white')
        self.beginspy.pack(side=LEFT)
        
    #creates the gesture list box and binds the event of selecting an element from that box to the function CurSelectG
    def CreateListBoxG(self):
        self.GFrame=Frame(self.OW)
        self.GFrame.pack(side=LEFT)
        self.listboxG = Listbox(self.GFrame,selectmode=SINGLE)
        self.listboxG.pack(side=LEFT)
        self.listboxG.bind('<<ListboxSelect>>',self.CurSelectG)
        
    #creates the mapping list box and binds the event of selecting an element from that box to the function CurSelectM
    def CreateListBoxM(self):
        self.MFrame=Frame(self.OW)
        self.MFrame.pack(side=LEFT)
        self.listboxM = Listbox(self.MFrame)
        self.listboxM.pack(side=LEFT)
        self.listboxM.bind('<<ListboxSelect>>',self.CurSelectM)
        
    #creates the user profile list box and binds the event of selecting an element from that box to the function CurSelect
    def CreateListBox(self):
        self.origFrame=Frame(self.OW)
        self.origFrame.pack(side=LEFT)
        self.listbox = Listbox(self.origFrame,selectmode=SINGLE)
        self.listbox.pack(side=LEFT)
        self.listbox.bind('<<ListboxSelect>>',self.CurSelect)
        self.create_add_button()

    def create_add_button(self):
        self.addb = Button(self.OW,text="+",command=self.userName)
        self.addb.pack(side=LEFT)
    
    #creates a window for users to enter their username for their profile
    def userName(self):
        self.username = Toplevel(self.OW)
        self.label = Label(self.username,text="Insert username")
        self.label.pack(side=LEFT)
        self.e1 = Entry(self.username)
        self.e1.pack(side=LEFT)
        self.okay = Button(self.username,text="Okay",bg='black',fg='white',command=lambda:[self.addToListBox(),self.quitUserbox()])
        self.okay.pack(side=LEFT)
        
    #adds usernames to list box to be accessed from there 
    def addToListBox(self):
        self.name = self.e1.get()
        self.listbox.insert(END, self.name)
        
    # the events that are activated when an item from userprofile listbox is selected
    def CurSelect(self,evt):
        value = str((self.listbox.get(ACTIVE)))
        UserProfiles.create_new(self,value)
        
    # the events that are activated when an item from gesture listbox is selected
    def CurSelectG(self,event):
        valueG = str((self.listboxG.get(ACTIVE)))
        UserProfiles.get_mapping(self,valueG)
        
    # the events that are activated when an item from mapping listbox is selected
    def CurSelectM(self,event):
        valueM = str((self.listboxG.get(ACTIVE)))
        UserProfiles.remove_mapping()
        
    # Destroying windows 
    def quitUserbox(self):
        self.username.destroy()
    def quitSplash(self):
        self.master.destroy()
    


        
#main
root = Tk()
spy_gui = GUI(root)
root.mainloop()

