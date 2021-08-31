import os
import json

def clear(command=False):
    with open("config.json", "r", encoding="utf-8") as configFile:
        config = json.load(configFile)
    if config["clear"] is True or command is True:
        os.system('cls' if os.name=='nt' else 'clear')