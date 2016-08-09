import requests
import json
import os
import importlib
from random import choice

from src.brain.brain import Brain


def interpret(message_object, bot_id):
    functions = [check_for_keywords, check_name]

    for func in functions:
        text, attachments = func(message_object)
        if text is not None or attachments is not None:
            respond(text, attachments, bot_id)
            break


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
        brain = Brain(message_object)
        return brain.who_said_that()

    else:
        return None, None


def respond(text, attachments, bot_id):
    template = {
                "bot_id": bot_id,
                "text": None,
                "attachments": []
                }
    if text is not None:
        template["text"] = str(text)
    if attachments is not None:
        template["attachments"].append(attachments)
    headers = {'content-type': 'application/json'}
    response = requests.post("https://api.groupme.com/v3/bots/post", data=json.dumps(template), headers=headers)
    print(response.status_code, response.reason)
