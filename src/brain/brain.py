import re
from nltk import word_tokenize, sent_tokenize



class Brain(object):
    def __init__(self, message_object):
        self.message_object = message_object

    def _normalize(self, text, attachments):

        emoji_pattern = re.compile('['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                               ']+', flags=re.UNICODE)

        # remove emojis
        emoji_pattern.sub('', text)

        # check for groupme powerup emojis
        if len(attachments) > 0:

            for i in attachments:

                if i['type'] == 'emoji':
                    # remove groupme powerup emojis
                    placeholder = int(text.find(i['placeholder']))
                    temp = list(text)
                    del temp[placeholder]
                    text = ''.join(temp)

        # remove urls
        text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}' \
                    '[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:' \
                    '[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]' \
                    '+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]' \
                    '+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                    '', text, flags=re.MULTILINE)

        # remove anything in parentheses or brackets
        text = re.sub('\(\w*\)', '', text)
        text = re.sub('\[\w*\]', '', text)

        # remove special characters
        special = '@~`^*<>{}_|\"'
        text = ''.join(c for c in text if c not in special)

        return text


    def _untokenize(self, words):
        """
        Untokenizing a text undoes the tokenizing operation, restoring
        punctuation and spaces to the places that people expect them to be.
        Ideally, `untokenize(tokenize(text))` should be identical to `text`,
        except for line breaks.
        """
        text = ' '.join(words)
        step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...').replace('# ', '#')
        step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
        step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
        step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
        step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
        step6 = step5.replace(" ` ", " '")
        return step6.strip()


    def who_said_that(self):
        sender = self.message_object.name
        s = self._normalize(self.message_object.text, self.message_object.attachments)
        response = []
        for name in word_tokenize(s):
            if name.lower() == "jarvis":
                response.append(sender.split(' ')[0])
            else:
                response.append(name)
        text = self._untokenize(response)
        return text, None
