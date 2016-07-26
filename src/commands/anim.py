import requests
import ast


def main(message_object):
    api_url = 'http://api.giphy.com/v1/gifs/translate?s=%s&api_key=dc6zaTOxFJmzC'
    if message_object.text.find('/anim ') > -1:
        search = message_object.text.split('/anim ', 1)[1]
        try:
            r = requests.get(api_url % search.replace(' ', '+'))
            data = ast.literal_eval(r.text)
            url = data['data']['images']['downsized_medium']['url'].replace('\\', '')
            text = None
            attachment = {"type": "image", "url": url}
        except:
            text = "I don't think I should look that up."
            attachment = None
    else:
        text = "I'm not sure what you want me to look up."
        attachment = None
    return text, attachment

def help():
    text = "Command: /help\n" \
           "Description: Searches Giphy for an animated image\n" \
           "Usage: /anim {phrase}" 

    return text, None
