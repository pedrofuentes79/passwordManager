import json
from json.decoder import JSONDecodeError
import os

from first_time import first_time_check
def test():
    with open("config.json", "r+") as f:
        try:
            config = json.load(f)
            if config["firstTime"] == "true":
                return True
            elif config["firstTime"] == "false":
                return False
        #In the case the file has not content due to the fact that it has just been created,
        #this code sets the info needed
        except JSONDecodeError:
            json_content = json.dumps({"firstTime": "true"})
            f.write(json_content)
            return True

def change_first_time():
    with open("config.json", "r+") as f:
        content = json.load(f)
        if content['firstTime'] == "true":
        # json_content = json.dumps({"firstTime": "false"})
        # f.write(json_content)
            content['firstTime'] = "false"
            json.dump(content, f, indent=4)
        elif content['firstTime'] == "false":
            content['firstTime'] = "true"
            json.dump(content, f, indent=4)


def testagain():
    with open('config.json') as f:
        config = json.load(f)

    with open('data.json', 'w') as f:
        json.dump(config, f)



def change_first_time_old():
    filename = "config.json"
    with open(filename, "r+") as f:
        config = json.load(f)
        config["firstTime"] = "false"
    with open(filename, "r+") as f:
        json.dump(config, f)

change_first_time_old()

