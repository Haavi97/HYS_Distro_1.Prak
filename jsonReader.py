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


if __name__ == '__main__':
    print(read_json())
    write_json({'c': '3'})
    print(read_json())
