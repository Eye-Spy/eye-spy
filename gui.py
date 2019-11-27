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
    def add_mapping():
        return
    def remove_mapping():
        return
    def get_mapping():
        return
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
        self.beginEyeButton()
        self.CreateListBox()

    def beginEyeButton(self):
        self.tFrame = Frame(self.OW)
        self.tFrame.pack()
        self.bFrame = Frame(self.OW)
        self.bFrame.pack(side=BOTTOM)
        self.beginspy = Button(self.bFrame, text = "Begin Eye Spy",bg ='black',fg='white')
        self.beginspy.pack(side=LEFT)

    def CreateListBox(self):
        self.listbox = Listbox(self.OW)
        self.listbox.pack(side=LEFT)
        self.addb = Button(self.OW,text="+",command=self.userName)
        self.addb.pack(side=LEFT)
        #self.listbox.insert(END,self.s)
    def userName(self):
        self.username = Toplevel(self.OW)
        self.label = Label(self.username,text="Insert username")
        self.label.pack(side=LEFT)
        self.e1 = Entry(self.username)
        self.e1.pack(side=LEFT)
        self.okay = Button(self.username,text="Okay",bg='black',fg='white',command=self.addToListBox)
        self.okay.pack(side=LEFT)

    def addToListBox(self):
        self.name = self.e1.get()
        self.listbox.insert(END, self.name)
        

root = Tk()
spy_gui = GUI(root)
root.mainloop()
