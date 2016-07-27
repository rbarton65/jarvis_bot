from random import choice


def main(message_object):
    if message_object.text.find('/8ball ') > -1:
        possible_responses = [
                            "It is certain.",
                            "It is decidedly so.",
                            "Without a doubt.",
                            "Yes, definitely.",
                            "You may rely on it.",
                            "As I see it, yes.",
                            "Most likely.",
                            "Outlook good.",
                            "Yes",
                            "Signs point to yes.",
                            "Reply hazy, try again.",
                            "Ask again later.",
                            "Better not tell you now.",
                            "Cannot predict now.",
                            "Concentrate and ask again.",
                            "Don't count on it.",
                            "My reply is no.",
                            "My sources say no.",
                            "Outlook not so good.",
                            "Very doubtful."
                            ]
        text = choice(possible_responses)
        return text, None
    else:
        text = "I need a question to respond properly."
        attachment = None
    return text, attachment


def help():
    text = "Command: /8ball\n" \
           "Description: Responds to a yes or no question\n" \
           "Usage: /8ball {question}"

    return text, None
