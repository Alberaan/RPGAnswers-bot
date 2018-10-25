import telepot
from telepot.loop import MessageLoop
import argparse
from configparser import SafeConfigParser
import requests
import json

def toTextList(data):
    text = ""

    for element in data["data"]:
        myelement = element.replace(".yml", "")
        text = text + myelement + "\n"

    return text

def listRequest(msg):
    command = msg['text']
    basicurl = "https://hall.herokuapp.com/api/types"

    arguments = command.replace("/list", "")
    options = arguments.split(" ")
    options.pop(0)

    checkError = False

    if len(options) == 0:
        header = "These are the available languages:\n"
    elif len(options) == 1:
        header = "These are the available systems for language " + options[0] + ":\n"
    elif len(options) == 2:
        header = "These are the available tables for language " + options[0] + " and system " + options[1] + ":\n"
    else:
        header = "Incorrect number of parameters for listing available options.\n" 

    for parameter in options:
        basicurl+="/" + parameter

    url = basicurl + ".json"

    r = requests.get(url = url)

    try:
        data = r.json()

        text = ""

        if ("succes" in data and data["succes"] == True) or ("success" in data and data["success"] == True):
            response = header + toTextList(data)
        else:
            response = header + "No available data."

    except ValueError:
        response = header + "Could not process your request."

    sendData(msg, bot, response)

def indent(level):
    indentation = ""

    for i in range(0, level):
        indentation += "-"

    return indentation

def jsonToTextGen(data):
    element = data["data"][0]

    return formatJSON(element, None, 0)

def formatJSON(element, parent, level):
    text = ""
    for key, value in element.items():
        if key == "text":
            if level < 1:
                text += value + "\n"
            else:
                text += indent(level) + parent["text"] + ": " + value + "\n"

        elif key == "related":
            for key2, value2 in value.items():
                text += formatJSON(value2["results"][0], value2, level+1)

    return text
    
def genRequest(msg):
    command = msg['text']
    basicurl = "https://hall.herokuapp.com/api/random"

    arguments = command.replace("/gen", "")
    options = arguments.split(" ")
    options.pop(0)

    for parameter in options:
        basicurl+="/" + parameter

    url = basicurl + ".json"
    r = requests.get(url)

    data = r.json()
    text = jsonToTextGen(data)
    
    sendData(msg, bot, text)

def sendData(msg, bot, data):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, data)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text' :
        if msg['text'].startswith("/list"):
           listRequest(msg) 
        if msg['text'].startswith("/gen"):
           genRequest(msg) 


# Main starts here
# Argument parsing.
parser = argparse.ArgumentParser(description='Welcome to RPGAnswers bot')
 
parser.add_argument('configFile', help='Config file for loading all parameters')
args = parser.parse_args()


# Using config file for parameters
parser = SafeConfigParser()
parser.read(args.configFile)

token = parser.get('token', 'telegram_token')

bot = telepot.Bot(token) # Bot is created from the telepot class


MessageLoop(bot, handle).run_as_thread()

while(1):
    pass
