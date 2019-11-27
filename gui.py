
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
        
    def add_mapping(self):
        return
    def remove_mapping(self):
        return
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

    def CreateListBoxG(self):
        self.listboxG = Listbox(self.OW)
        self.listboxG.pack(side=LEFT)
        self.listboxG.bind("<<ListboxSelect>>",self.CurSelectG)

    def CreateListBoxM(self):
        self.listboxM = Listbox(self.OW)
        self.listboxM.pack(side=LEFT)
        self.listboxM.bind("<<ListboxSelect>>",self.CurSelectM)

    def CreateListBox(self):
        self.listbox = Listbox(self.OW)
        self.listbox.pack(side=LEFT)
        self.listbox.bind("<<ListboxSelect>>",self.CurSelect)
        self.create_add_button()

    def create_add_button(self):
        self.addb = Button(self.OW,text="+",command=self.userName)
        self.addb.pack(side=LEFT)
        
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
    def CurSelect(self,evt):
        #self.press = event.press
        value = str((self.listbox.get(ACTIVE)))
        UserProfiles.create_new(self,value)
    def CurSelectG(self,event):
        valueG = str((self.listboxG.get(ACTIVE)))
        UserProfiles.get_mapping(self,valueG)
    def CurSelectM(self,event):
        valueM = str((self.listboxG.get(ACTIVE)))
        UserProfiles.remove_mapping()
    # Destroying windows 
    def quitUserbox(self):
        self.username.destroy()
    def quitSplash(self):
        self.master.destroy()
    


        

root = Tk()
spy_gui = GUI(root)
root.mainloop()

