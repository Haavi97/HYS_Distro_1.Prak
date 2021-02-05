import json

path = 'data.json'


def read_json():
    with open(path) as file:
        json_data = json.load(file)
    return json_data


def write_json(new_data):
    current_json = read_json()
    current_json["data"].append(new_data)
    with open(path, 'w') as f:
        json.dump(current_json, f)
