import requests
import ast


def main(message_object):
    '''Searches Wikipedia for a summary of a topic'''
    api_url = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=%s&format=json&callback=?'

    # check if there is a space after command,
    # showing there's something that comes after
    if message_object.text.find('/wiki ') > -1:
        search = message_object.text.split('/wiki ', 1)[1]

        try:
            r = requests.get(api_url % search.replace(' ', '+'))
            data = ast.literal_eval(r.content.decode('UTF-8')[4:])
            text = data[2][0]
            attachment = None

        except:
            text = "I don't think I should look that up."
            attachment = None

    else:
        text = "I'm not sure what you want me to look up."
        attachment = None

    return text, attachment


def help():
    '''Gives help text when called by help.py'''
    text = "Command: /wiki\n" \
        "Description: Searches Wikipedia for a summary of a topic\n" \
        "Usage: /wiki {topic}"

    return text, None
