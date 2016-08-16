import requests
import json
import os
import importlib
from random import choice

from src.brain.brain import Brain


def interpret(message_object, bot_id):
    functions = [shut_up_meg, check_for_keywords, check_name]

    for func in functions:
        text, attachments = func(message_object)
        if text is not None or attachments is not None:
            print("going to respond")
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
    brain = Brain(message_object)
    if lowercase.find("jarvis") > -1:      
        return brain.generate_response()
    else:
        if choice(range(19)) == 14:
            return brain.generate_response()
        else:
            brain.add_to_db()
            return None, None
            
            
def shut_up_meg(message_object):
    if message_object.user_id == "2994974" and choice(range(14)) == 7:
        return "Shut up, Meg.", None
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

