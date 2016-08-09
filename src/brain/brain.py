import re
from nltk import word_tokenize


class Brain(object):
    def __init__(self, message_object):
        self.message_object = message_object

    def _untokenize(self, words):
        """
        Untokenizing a text undoes the tokenizing operation, restoring
        punctuation and spaces to the places that people expect them to be.
        Ideally, `untokenize(tokenize(text))` should be identical to `text`,
        except for line breaks.
        """
        text = ' '.join(words)
        step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
        step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
        step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
        step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
        step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
        step6 = step5.replace(" ` ", " '")
        return step6.strip()

    def who_said_that(self):
        sender = self.message_object.name
        s = self.message_object.text
        response = []
        for name in word_tokenize(s):
            if name.lower() == "jarvis":
                response.append(sender.split(' ')[0])
            else:
                response.append(name)
        print(response)
        text = self._untokenize(response)
        return text, None
