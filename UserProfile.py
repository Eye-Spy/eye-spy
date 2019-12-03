import json
import os
from tkinter import *
import GestureNames

class UserProfile():

    def populate_profile_listbox(listbox):
        """
        Dynamically populates the User Profile names into the User Profile listbox in the GUI

        Access the config.json file and inserts each profile_id into the User Profile listbox

        Parameters:
        listbox: a reference to the User Profile listbox object

        Returns:
        None
        """
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                for each in data['user_profiles']:
                    listbox.insert(END, each['profile_id'])
        except (IndexError):
                return

    def populate_gestures_listbox(listbox):
        """
        Dynamically populates the Gesture names into the Gesture listbox in the GUI

        Access the GestureNames file and inserts each name in the 
        gesture name dictionary into the Gestures listbox

        Parameters:
        listbox: a reference to the Gesture listbox object

        Returns:
        None
        """
        try:
            for each in GestureNames.gesture_name_dict.values():
                listbox.insert(END, each)
        except (IndexError):
                return

    def populate_mappings_listbox(listbox, profile_id, gesture_id):
        """
        Dynamically populates the application mappings into the application mappings listbox in the GUI

        Access the config.json file and inserts each application mapping into the application mapping listbox

        Parameters:
        listbox: a reference to the Application Mappings listbox object
        profile_id: id of the currently selected User Profile
        gesture_id: id of the currently selected Gesture to which the applications are mapped

        Returns:
        None
        """
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                for each in data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings']:
                    listbox.insert(END, os.path.basename(os.path.splitext(each)[0]))
        except (IndexError):
                return

    def change_profile_id(index_profile_id, new_Username):
        """
        Changes the profile_id value of the currently selected User Profile

        Access the config.json file and replace the current profile_id value with the new_Username

        Parameters:
        index_profile_id: index of the currently selected profile
        new_Username: the username string that is to replace the profile_id value for the selected profile

        Returns:
        None
        """
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                data['user_profiles'][index_profile_id]['profile_id'] = new_Username
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (IndexError):
                return

    def clear_profile(profile_id):
        """
        Removes all of the application mappings and profile_id for the selected User Profile

        Access the config.json file and deletes application mappings and profile_id
        for the currently selected User Profile

        Parameters:
        profile_id: id of the currently selected User Profile

        Returns:
        None
        """
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                data['user_profiles'][profile_id]['profile_id'] = ("User Profile " + str(profile_id + 1))
                for gestures in data['user_profiles'][profile_id]['gestures']:
                        del gestures['mappings'][:]   
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (IndexError):
                return

    def add_mapping(profile_id, gesture_id, application):
        """
        Adds the application to the Application Mappings list

        Access the config.json file and add the application mapping of application for the 
        currently selected User Profile and Gesture

        Parameters:
        profile_id: id of the currently selected User Profile
        gesture_id: id of the currently selected Gesture to which the applications are mapped
        application: string name of the application mapping to be added

        Returns:
        None
        """
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                if application not in data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings'] and application:
                    data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings'].append(application)
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (IndexError):
                return
    def remove_mapping(profile_id, gesture_id, application_id):
        """
        Deletes the currently selected mapping from the Application mappings list

        Access the config.json file and remove the application mapping for the 
        currently selected User Profile and Gesture

        Parameters:
        profile_id: id of the currently selected User Profile
        gesture_id: id of the currently selected Gesture to which the applications are mapped
        application_id: id of the application mapping to be removed

        Returns:
        None
        """
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                del data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings'][application_id]
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (IndexError):
                return

    def get_mapping(profile_id, gesture_id):
        """
        Retrieves the mappings list from config.json

        Access the config.json file and retrieves the application mappings list 
        for the currently selected User Profile and Gesture

        Parameters:
        profile_id: id of the currently selected User Profile
        gesture_id: id of the currently selected Gesture to which the applications are mapped

        Returns:
        List of Applications for the currently selected User Profile and Gesture
        """
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                return data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings']
        except (IndexError):
                return
