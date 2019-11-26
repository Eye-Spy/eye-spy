import json
class UserProfile():

    def __init__(self):
        return

    def to_dict(self):
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
