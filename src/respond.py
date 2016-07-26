import requests
import json
import os
import importlib
import string


def interpret(message_object):
    functions = [check_for_keywords, check_name]
    
    for func in functions:
        text, attachments = func(message_object)
        if text is not None or attachments is not None:
            respond(text, attachments)
            break


def who_said_that(message_object):
    sender = message_object.name
    sender_id = message_object.user_id

    attachments = {
                   "loci": [[0, 12]],
                   "type": "mentions",
                   "user_ids": None
                   }

    attachments["user_ids"] = [sender_id]
    text = "@%s said this" % sender
    return text, attachments


def check_for_keywords(message_object):
    '''Check for any commands in the text'''
    filename = os.path.join(os.path.dirname(__file__), 'commands.txt')
    command_file = open(filename, 'r')
    commands = [line.replace('\n', '') for line in command_file.readlines()]

    for command in commands:
        if message_object.text.find("/%s" % command) > -1:
            module = importlib.import_module("src.commands.%s" % command)
            importlib.reload(module)
            return module.main(message_object)
        else:
            pass

    return None, None


def check_name(message_object):
    lowercase = message_object.text.lower()
    if lowercase.find("jarvis") > -1:
        text = "Hello! Jarvis is undergoing some maintanance right now. In the meantime, \
                my name is Wilson. I am able to perform /anim and /question commands."    
    else:
        text = None
    
    return text, None

def respond(text, attachments=None):
    bot_id = ""
    template = {
                "bot_id": None,
                "text": None,
                "attachments": []
                }

    template["bot_id"] = bot_id
    if text is not None:
        template["text"] = str(text)
    if attachments is not None:
        template["attachments"].append(attachments)
    headers = {'content-type': 'application/json'}
    response = requests.post("https://api.groupme.com/v3/bots/post", data=json.dumps(template), headers=headers)
    print(response.status_code, response.reason)
