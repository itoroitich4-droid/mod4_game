from utils.file_handler import read_json, write_json


def register(username):
    data = read_json("data/users.json")

    for user in data["users"]:
        if user["username"] == username:
            return False

    data["users"].append({
        "username": username,
        "score": 0
    })

    write_json("data/users.json", data)

    return True


def login(username):
    data = read_json("data/users.json")

    for user in data["users"]:
        if user["username"] == username:
            return True

    return False


def get_user(username):
    data = read_json("data/users.json")

    for user in data["users"]:
        if user["username"] == username:
            return user

    return None


def update_score(username, score):
    data = read_json("data/users.json")

    for user in data["users"]:
        if user["username"] == username:

            if score > user["score"]:
                user["score"] = score

    write_json("data/users.json", data)