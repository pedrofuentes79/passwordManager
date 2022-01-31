from io import UnsupportedOperation
import json
import os

def first_time_check():
    with open("config.json", "w") as f:
        try:
            config = json.load(f)
            if config["firstTime"] == "true":
                return True
            elif config["firstTime"] == "false":
                return False
        except UnsupportedOperation:
            #In the case the file has not content due to the fact that it has just been created,
            #this code sets the info needed
            json_content = json.dumps({"firstTime": "true"})
            f.write(json_content)
            return True

def change_first_time():
    filename = "config.json"
    with open(filename, "r+") as f:
        config = json.load(f)
        config["firstTime"] = "false"
    with open(filename, "r+") as f:
        json.dump(config, f)
