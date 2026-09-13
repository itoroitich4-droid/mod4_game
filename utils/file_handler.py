import json


def read_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def write_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_questions():
    return read_json("data/questions.json")