import json
import os
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
                return

    def populate_gestures_listbox(listbox):
        try:
            for each in GestureNames.gesture_dict.values():
                listbox.insert(END, each)
        except (IndexError):
                return

    def populate_mappings_listbox(listbox, profile_id, gesture_id):
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                for each in data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings']:
                    listbox.insert(END, os.path.basename(os.path.splitext(each)[0]))
        except (IndexError):
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
                return

    def clear_profile(profile_id):
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
        try:
            with open('./config.json', 'r') as mappings:
                data = json.load(mappings)
                return data['user_profiles'][profile_id]['gestures'][gesture_id]['mappings']
        except (IndexError):
                return
