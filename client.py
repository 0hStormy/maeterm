import requests
import json
import getpass
import platform
import os
from websockets.sync.client import connect

class fg:
    red = "\x1b[1;31m"
    yellow = "\x1b[1;33m"
    green = "\x1b[1;32m"
    blue = "\x1b[1;34"

class ex:
    reset = "\x1b[0m"

def cprint(message, color):
    print(f"{color}{message}{ex.reset}")

def read(key):
    with open("config.json", "r") as f:
        dat = f.read()
        jsondat = json.loads(dat)
        return jsondat[key]

# Determine clear command
def clear():
    if platform.system() == 'Windows':
        clearCMD = 'cls'
    else:
        clearCMD = 'clear'
    os.system(clearCMD)

def auth():
    user = input("Username: ")
    password = getpass.getpass("Password: ")

    sendJSON = {
        "username": user,
        "password": password
    }

    login = requests.post(f"{httpUrl}/login", json.dumps(sendJSON))
    try:
        jsonResponse = login.json()
        return jsonResponse["token"]
    except KeyError:
        print("Incorrect username or password!")

def getPosts(useCache=True):
    ws = {
        "cmd": "fetch",
        "offset": 0
    }

    if useCache is False:
        with connect(read("ws_url")) as websocket:
            websocket.send(json.dumps(ws))
            message = websocket.recv()
            with open(".cache", "w") as f:
                f.write(message)
    else:
        with open(".cache", "r") as f:
            message = f.read()
    for post in json.loads(message)["posts"]:
        postBody = post["p"]
        postUser = post["u"]
        cprint(f"{postUser}:", fg.red)
        print(postBody)

global httpUrl
httpUrl = read("http_url")

clear()
cprint("Welcome to Maeterm!", fg.red)
token = auth()

getPosts(useCache=False)
while True:
    clear()
    getPosts()
    cmd = input(":")
    match cmd:
        case "exit":
            exit(0)
        case "post":
            postContent = input("Type message: ")
            ws = {
                "cmd": "post",
                "token": token,
                "p": postContent
            }
            with connect(read("ws_url")) as websocket:
                websocket.send(json.dumps(ws))
                message = websocket.recv()
                getPosts(useCache=False)
        case "r":
            getPosts(useCache=False)
        case _:
            cprint("Invalid command!", fg.red)