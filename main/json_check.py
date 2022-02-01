try: 
    with open("config.json", "x"):
        pass
except FileExistsError:
    pass
