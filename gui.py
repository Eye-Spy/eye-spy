
from tkinter import *
from tkinter import filedialog
from UserProfile import UserProfile 
import GestureNames
from WebcamHandler import WebcamHandler

class GUI:
    def __init__(self, master):
        """
        Constructor method for the GUI class.
        
        Creates Splash Screen and calls the function that opens the operational window. 
        
        Parameters:
        master(object): a reference to the root tkinter object created in the main.
        
        Returns:
        None
        """
        self.master = master
        self.webcam_Gesture = None
        self.webcam_running = False
        master.title("Eye Spy")
        master.configure(background = 'grey')
        self.banner = PhotoImage(file="Gesture_Photos/Eye_spy.png")
        self.B = Button(master,image = self.banner, command = self.openNew)
        self.B.pack()
    
    #opens the operational window and calls the begin eye spy button function and creates the list box for user profiles    
    def openNew(self):
        """
        Creates the operational window with frames for each button. 
        
        Calls the listbox functions for UserProfiles, Gestures and Mappings. 
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.B['state'] = DISABLED
        self.tFrame = Frame(self.master)
        self.tFrame.pack(side=RIGHT)
        self.pFrame = Frame(self.master)
        self.pFrame.pack(side=LEFT)
        self.bFrame = Frame(self.master)
        self.bFrame.pack(side=BOTTOM)
        self.spyFrame = Frame(self.bFrame)
        self.spyFrame.pack(side=BOTTOM)
        self.beginspy = Button(self.spyFrame, text = "Begin Eye Spy",bg ='white',fg='black', command=self.StartWebcamHandler)
        self.beginspy.pack(side=LEFT)
        self.endspy = Button(self.spyFrame, text = "Stop Eye Spy",bg ='white',fg='black', command=self.StopWebcamHandler)
        self.endspy.pack(side=RIGHT)
        self.CreateListBox_Profiles()
        self.CreateListBox_Gestures()
        self.CreateListBox_Mappings()
        self.Gesture_Photo()


    #creates the user profile list box and binds the event of selecting an element from that box to the function CurSelect
    def CreateListBox_Profiles(self):
        """
        Creates the user profile list box 
        
        Calls a function from the UserProfile class that populates the listbox with default settings
        
        Calls the change_username function 
        
        Binds the event of selecting an element from that box to the function ProfileBinds
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.origFrame=Frame(self.pFrame)
        self.origFrame.pack(side=TOP)
        self.listbox = Listbox(self.origFrame, selectmode=SINGLE, exportselection=False)
        self.listbox.pack(side=LEFT)
        self.change_frame=Frame(self.pFrame)
        self.change_frame.pack(side=BOTTOM)
        UserProfile.populate_profile_listbox(self.listbox)
        self.change_username()
        self.listbox.bind('<<ListboxSelect>>',self.ProfileBinds)

    
    #create add button
    def change_username(self):
        """
        Creates buttons for clearing and changing user profiles
        
        Calls the userName function
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.clear_profile = Button(self.change_frame,text="Clear Profile Name & Settings", command=self.Clear)
        self.clear_profile.pack(side=RIGHT)
        self.change_username = Button(self.change_frame,text="Change User Profile Name", command=self.userName)
        self.change_username.pack(side=LEFT)

    #creates a window for users to enter their username for their profile
    def userName(self):
        """
        Creates a new window and prompts users to add a username 
        
        Calls the addToListBox function
        
        Parameters:
        None
        
        Returns:
        None
        """
        try:
            shitty_error_check = self.listbox.curselection()[0]
            self.username = Toplevel(self.master)
            self.label = Label(self.username,text="Insert username")
            self.label.pack(side=LEFT)
            self.e1 = Entry(self.username)
            self.e1.pack(side=LEFT)
            self.okay = Button(self.username,text="Okay",bg='white',fg='black',command=lambda:[self.addToListBox(self.listbox.curselection()[0]),self.username.destroy()])
            self.okay.pack(side=LEFT)
        except(IndexError):
            return
    
    #adds usernames to list box to be accessed from there 
    def addToListBox(self, selection):
        """
        Adds the username inputted by the user to the userprofile listbox. 
        
        Calls a method from the UserProfile class to change the profile id of the default settings, so the name the user inputted
        
        Parameters:
        selection(object): The selected default user profile to be changed. 
        
        Returns:
        None
        """
        self.name = self.e1.get()
        UserProfile.change_profile_id(selection, self.name)
        self.listbox.delete(0,END)     
        UserProfile.populate_profile_listbox(self.listbox)

    
    def CreateListBox_Gestures(self):
        """
        Creates the Gestures list box 
        
        Calls a function from the UserProfile class that populates the listbox with default gesture settings
        
        Binds the event of selecting an element from that box to the function GestureBinds
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.orig=Frame(self.origFrame)
        self.orig.pack(side=LEFT)
        self.listboxG = Listbox(self.orig,selectmode=SINGLE, exportselection=False)
        self.listboxG.pack(side=LEFT)
        UserProfile.populate_gestures_listbox(self.listboxG)
        self.listboxG.bind('<<ListboxSelect>>', self.GestureBinds)

    def CreateListBox_Mappings(self):
        """
        Creates the mappings list box 
        
        Creates a frame for the add and remove buttons and calls the Add_Remove_buttons function
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.ori=Frame(self.origFrame)
        self.ori.pack(side=LEFT)
        self.listboxM = Listbox(self.ori,selectmode=SINGLE,  exportselection=False)
        self.listboxM.pack(side=LEFT)
        self.buttons=Frame(self.master)
        self.buttons.pack(side=LEFT)
        self.Add_Remove_buttons()

    def Add_Remove_buttons(self):
        """
        Creates the Add and Remove buttons
        
        Calls the add_mapping function and the remove_mapping button depending on which button is pressed by the user. 
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.Add = Button(self.buttons,text="+", command=self.add_mapping)
        self.Remove = Button(self.buttons,text="-", command=self.remove_mapping)
        self.Add.pack(side=TOP)
        self.Remove.pack(side=BOTTOM)
        self.Add['state'] = DISABLED
        self.Remove['state'] = DISABLED
        
    def add_mapping(self):
        """
        Opens the file browser that allows users to browse through their applications and select which one they want to use. 
        
        Calls the add_mapping method from the UserProfile class that takes in the selected user profile, gesture and application 
        
        Calls the populate_mapping_listbox function from the UserProfile class that populates the list box with the application name
        
        Parameters:
        None
        
        Returns:
        None
        """
        try:
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes = (("exe",".exe"), ("App", ".app"), ("Bash Scripts", ".sh"), ("All Files","*.*")))
            UserProfile.add_mapping(self.listbox.curselection()[0], self.listboxG.curselection()[0], self.filename)
            self.listboxM.delete(0,END)    
            UserProfile.populate_mappings_listbox(self.listboxM, self.listbox.curselection()[0], self.listboxG.curselection()[0])
        except(IndexError):
            return

    def remove_mapping(self):
        """
        Removes the mapping that is selected by the user. 
        
        Parameters:
        None
        
        Returns:
        None
        """
        try:
            UserProfile.remove_mapping(self.listbox.curselection()[0], self.listboxG.curselection()[0], self.listboxM.curselection()[0])
            self.listboxM.delete(0,END)    
            UserProfile.populate_mappings_listbox(self.listboxM, self.listbox.curselection()[0], self.listboxG.curselection()[0])
        except(IndexError):
            return

    def Clear(self):
        """
        Calls the clear_profile function from the UserProfile class
        
        Resets the Selected profile to the original default settings 
        
        Parameters:
        None
        
        Returns:
        None
        """
        try:
            UserProfile.clear_profile(self.listbox.curselection()[0])
            self.listbox.delete(0, END)
            self.listboxG.delete(0, END)
            self.listboxM.delete(0, END)
            UserProfile.populate_profile_listbox(self.listbox)
            UserProfile.populate_gestures_listbox(self.listboxG)
        except(IndexError):
            return

    def Gesture_Photo(self):
        """
        Creates a frame for the gesture photos.
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.picFrame = Frame(self.master)
        self.picFrame.pack()

    def GestureBinds(self,evt):
        """
        Calls Photo_Change and CurSelect functions 
        
        Parameters:
        evt(event): When the user selects an element of the gesture listbox
        
        Returns:
        None
        """
        self.Photo_Change()
        self.CurSelect()
    def ProfileBinds(self,evt):
        """
        Calls CurSelect function when element from the userprofile listbox is selected. 
        
        Parameters:
        evt(event): When an element of user profile listbox is selected. 
        
        Returns:
        None
        """
        self.CurSelect()

    def Photo_Change(self):
        """
        Displays the picture that corressponds to each gesture that the user selects.
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.picFrame.destroy()
        self.picFrame = Frame(self.master)
        self.picFrame.pack()
        path = "Gesture_Photos/"+GestureNames.gesture_file_dict[self.listboxG.curselection()[0]]+".png"
        self.gesturepic=PhotoImage(file=path)
        self.photo=Button(self.picFrame, image=self.gesturepic)
        self.photo.pack()

    def get_profile(self):
        """
        Gets the profile from the userprofile listbox that the user selects.
        
        Parameters:
        None
        
        Returns:
        None
        """
        return self.listbox.curselection()[0]

    def CurSelect(self):
        """
        Calls the populate_mappings_listbox function from the class UserProfile and activates the add and remove buttons
        
        Parameters:
        None
        
        Returns:
        None
        """
        try:
            self.listboxM.delete(0,END)    
            UserProfile.populate_mappings_listbox(self.listboxM, self.listbox.curselection()[0], self.listboxG.curselection()[0])
            self.Add['state'] = NORMAL
            self.Remove['state'] = NORMAL
        except(IndexError):
            return
    
    def StartWebcamHandler(self):
        """
        calls the webcam_Gesture function and starts the webcam based on the profile that is selected at the time.
        
        Parameters:
        None
        
        Returns:
        None
        """
        try:
            self.webcam_Gesture = WebcamHandler(profile=self.listbox.curselection()[0])
            self.webcam_Gesture.start()
        except(IndexError):
            return

        #Backend.action_On_Gesture(self.webcam_Gesture, self.listbox.curselection()[0])

    def StopWebcamHandler(self):
        """
        Stops the webcam. 
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.webcam_running = False
        self.webcam_Gesture.close()
    
#    def display_webcam(self):
#        if self.webcam_Gesture and type(self.webcam_Gesture.cur_image) is np.ndarray:
#            cv2.imshow("Webcam", self.webcam_Gesture.cur_image)
#        root.after(5, self.display_webcam)

        
#main
root = Tk()
spy_gui = GUI(root)
#root.after(5, spy_gui.display_webcam)
root.mainloop()
