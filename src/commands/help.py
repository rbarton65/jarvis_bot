import importlib


def main(message_object):
    '''Provides description on available commands'''
    command_file = open('src/commands.txt', 'r')
    commands = [line.replace('\n', '') for line in command_file.readlines()]

    if message_object.text.find('/help ') > -1:
        # Check if command is active in command list
        search = message_object.text.split('/help ', 1)[1]

        if search == "help":
            loci = len(message_object.name) + 1
            text = "Hey everyone, @%s is trying to be " \
                    "funny asking for help on the help " \
                    "command. Hint, you're not." % message_object.name
            attachments = {
                   "loci": [[14, loci]],
                   "type": "mentions",
                   "user_ids": [message_object.user_id]
                   }
            return text, attachments

        for command in commands:

            if search.find(command) > -1:
                module = importlib.import_module("src.commands.%s" % command)
                importlib.reload(module)
                return module.help()

            else:
                pass

        text = "This command is not available. For a list" \
                "of available commands, type '/help'"

        return text, None

    else:
        text = "Available Commands:\n%s" % ('\n'.join(commands))

        return text, None
