import json

def first_time_check():
    '''
    Checks if this is the first time the user has opened the application.
    If it is, show the "sign up" page, otherwise the login one.
    '''
    try:
        with open("config.json", "r+") as f:

            config = json.load(f)
            if config["firstTime"] == "true":
                return True
            else:
                return False
    except FileNotFoundError:
        with open("config.json", "w") as f:
            f.write(json.dumps({"firstTime": "true"}))
            return True

def change_first_time_to_false():
    '''
    Changes firstTime to false when the user has already signed up
    '''
    config = json.load(open("config.json"))
    if config["firstTime"] == "true":
        config.pop("firstTime")
        config["firstTime"] = "false"
    open("config.json", "w").write(json.dumps(config))

            

