import json
from tkinter import *
import GestureNames

class UserProfile():

    def __init__(self):
        return

    def populate_profile_listbox(listbox):
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                for each in data['user_profiles']:
                    listbox.insert(END, each['profile_id'])
        except (IndexError):
                #handle what happens when we have greater than 10 user profiles
                return

    def populate_gestures_listbox(listbox):
        try:
            for each in GestureNames.gesture_dict.values():
                listbox.insert(END, each)
        except (IndexError):
                #handle what happens when we have greater than 10 user profiles
                return

    def populate_mappings_listbox(listbox, profile_id, gesture_id):
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                for each in data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings']:
                    listbox.insert(END, each)
        except (IndexError):
                #handle what happens when we have greater than 10 user profiles
                return

    def change_profile_id(index_profile_id, new_Username):
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                data['user_profiles'][index_profile_id]['profile_id'] = new_Username
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (IndexError):
                #handle what happens when we have greater than 10 user profiles
                return

    def add_mapping(profile_id, gesture_id, application):
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                data['user_profiles'][profile_id - 1]['gestures'][gesture_id - 1]['mappings'].append(application)
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (IndexError):
                print("Invalid Index Value")
        
    def remove_mapping(profile_id, gesture_id, application):
        try:
            with open('./config.json', 'r+') as mappings:
                data = json.load(mappings)
                data['user_profiles'][profile_id - 1]['gestures'][gesture_id - 1]['mappings'].remove(application)
                mappings.seek(0)
                json.dump(data, mappings, indent=4)
                mappings.truncate()
        except (ValueError):
                print("Invalid Application Value")

    def get_mapping(profile_id, gesture_id):
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                return data['user_profiles'][profile_id - 1]['gestures'][gesture_id - 1]['mappings']
        except (IndexError):
                print("Invalid Index Value")
