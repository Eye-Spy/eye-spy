
from tkinter import *
import platform
from UserProfile import UserProfile 

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Eye Spy")
        master.configure(background = 'grey')
        self.banner = PhotoImage(file="Eye spy.png")
        self.B = Button(master,image = self.banner, command = self.openNew)
        self.B.pack()
    
    #opens the operational window and calls the begin eye spy button function and creates the list box for user profiles    
    def openNew(self):
        self.B['state'] = DISABLED
        self.tFrame = Frame(self.master)
        self.tFrame.pack()
        self.pFrame = Frame(self.master)
        self.pFrame.pack(side=LEFT)
        self.bFrame = Frame(self.master)
        self.bFrame.pack(side=BOTTOM)
        self.beginspy = Button(self.bFrame, text = "Begin Eye Spy",bg ='white',fg='black')
        self.beginspy.pack(side=LEFT)
        self.CreateListBox_Profiles()
        self.CreateListBox_Gestures()
        self.CreateListBox_Mappings()


    #creates the user profile list box and binds the event of selecting an element from that box to the function CurSelect
    def CreateListBox_Profiles(self):
        self.origFrame=Frame(self.pFrame)
        self.origFrame.pack()
        self.listbox = Listbox(self.origFrame, selectmode=SINGLE, exportselection=False)
        self.listbox.pack(side=TOP)
        UserProfile.populate_profile_listbox(self.listbox)
        self.change_username()
        self.listbox.bind('<<ListboxSelect>>',self.CurSelect)

    
    def CreateListBox_Gestures(self):
        self.orig=Frame(self.master)
        self.orig.pack(side=LEFT)
        self.listboxG = Listbox(self.orig,selectmode=SINGLE, exportselection=False)
        self.listboxG.pack()
        UserProfile.populate_gestures_listbox(self.listboxG)
        self.listboxG.bind('<<ListboxSelect>>',self.CurSelect)


    def CreateListBox_Mappings(self):
        self.ori=Frame(self.master)
        self.ori.pack(side=LEFT)
        self.listboxM = Listbox(self.ori,selectmode=SINGLE,  exportselection=False)
        self.listboxM.pack()

    #create add button
    def change_username(self):
        self.change_username = Button(self.origFrame,text="Change User Profile Name", command=self.userName)
        self.change_username.pack(side=BOTTOM)

    #creates a window for users to enter their username for their profile
    def userName(self):
        self.username = Toplevel(self.master)
        self.label = Label(self.username,text="Insert username")
        self.label.pack(side=LEFT)
        self.e1 = Entry(self.username)
        self.e1.pack(side=LEFT)
        self.okay = Button(self.username,text="Okay",bg='white',fg='black',command=lambda:[self.addToListBox(),self.username.destroy()])
        self.okay.pack(side=LEFT)
    
    #adds usernames to list box to be accessed from there 
    def addToListBox(self):
        self.name = self.e1.get()
        #print(self.listbox.curselection())
        UserProfile.change_profile_id(self.listbox.curselection()[0], self.name)
        self.listbox.delete(0,END)     
        UserProfile.populate_profile_listbox(self.listbox)

    def CurSelect(self,evt):
        try:
            self.listboxM.delete(0,END)    
            UserProfile.populate_mappings_listbox(self.listboxM, self.listbox.curselection()[0], self.listboxG.curselection()[0])
        except(IndexError):
            return

        
        
#main
root = Tk()
spy_gui = GUI(root)
root.mainloop()