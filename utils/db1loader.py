import json

def load_data():
    with open("database/db1.json", "r") as file:
        return json.load(file)


#for  our games help and credit section read