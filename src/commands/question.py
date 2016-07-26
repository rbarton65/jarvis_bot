import wolframalpha
from random import choice


def main(message_object):
    if message_object.text.find('/question ') > -1:
        client = wolframalpha.Client('')
        search = message_object.text.split('/question ', 1)[1]
        try:
            result = client.query(search)
            print(next(result.results).img)
            if next(result.results).text is not None:
                text = next(result.results).text
                attachment = None
            else:
                text = None
                attachment = {"type": "image", "url": next(result.results).img}

        except:
            messages = ["Some things are better left unanswered.", "Why would you ask that?",
                        "No comment", "I don't work very well.", "I wasn't coded that well, sorry.",
                        "I can't answer that.", "Please go easy on me with these questions.",
                        "Don't blame me for not being able to answer, blame Meg."]
            text = choice(messages)
            attachment = None

    else:
        text = "I'm not sure what you want me to answer."
        attachment = None

    return text, attachment
