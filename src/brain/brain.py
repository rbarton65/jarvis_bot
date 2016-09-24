import re
import json
from ast import literal_eval
from random import choice
from nltk import word_tokenize, sent_tokenize

start = '<<START>>'
end = '<<END>>'

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
                               
        # check for groupme powerup emojis
        if len(attachments) > 0:
        
            for i in attachments:
            
                if i['type'] == 'emoji':
                    # remove groupme powerup emojis
                    placeholder = int(text.find(i['placeholder']))
                    temp = list(text)
                    del temp[placeholder]
                    text = ''.join(temp)

        # remove emojis
        emoji_pattern.sub('', text)

        # remove urls
        text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}' \
                    '[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:' \
                    '[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]' \
                    '+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]' \
                    '+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                    '', text, flags=re.MULTILINE)
        
        # remove anything in parentheses or brackets
        text = re.sub('\(.*?\)', '', text)
        text = re.sub('\[.*?\]', '', text)

        # remove special characters
        special = '@~`^*<>{}_|\"'
        text = ''.join(c for c in text if c not in special)
        
        return text
    
    def generate_response(self):
        s = self._normalize(self.message_object.text, self.message_object.attachments)
        markov = Markov(s, self.message_object.name)
        response = markov.generate_text()
        return response, None
    
    def add_to_db(self):
        s = self._normalize(self.message_object.text, self.message_object.attachments)
        markov = Markov(s, self.message_object.name)


class Markov(object):

    def __init__(self, message, sender):
        self.message = message.lower()
        self.sender = sender
        self.cache = self._fetch_brain()   
        self._database()
        self._write_brain()
    
    def _fetch_brain(self):
        print('finding brain')
        with open('src/brain/brain.json', 'r', encoding='utf-8') as json_file:
            try:
                brain = json.load(json_file)
            except:
                brain = {}
        db = {}
        for num,i in enumerate(brain):
            temp = literal_eval(i)            
            db[temp] = brain[i]
        return db
    
    def _write_brain(self):
        print('writing brain')
        brain = {}
        for i in self.cache:
            key = str(i)
            brain[key] = self.cache[i]
        with open('src/brain/brain.json', 'w') as json_file:
            json.dump(brain, json_file, indent=4,separators=(',', ':'))
        
    def _create_tuples(self):
        sentences = sent_tokenize(self.message)
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            if len(words) > 3:
                words = [start] + words
                words.append(end)
                for i in range(len(words) - 3):
                    yield(words[i], words[i+1], words[i+2], words[i+3])
            else:
                pass

    def _database(self):
        print('creating new database')
        for w1,w2,w3,w4 in self._create_tuples():
            key = (w1,w2,w3)
            print(key, w4)
            if key in self.cache:
                self.cache[key].append(w4)
            else:
                self.cache[key] = [w4]
    
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
    
    def generate_text(self):
        sentences = [i for i in sent_tokenize(self.message) if len(word_tokenize(i)) > 3]
        if len(sentences) < 1:
            response = word_tokenize(sent_tokenize(self.message)[0])
        
        else:
            response = []
            while True:
                words = word_tokenize(choice(sentences))
                seed = choice(range(len(words)-3))
                print(seed)
                if ('<<START>>', words[seed], words[seed+1]) in self.cache:
                    first_word, second_word, third_word = words[seed], words[seed+1], words[seed+2]
                    break
            
            
            while True:
                response.append(first_word)
                first_word, second_word, third_word = second_word, third_word, choice(self.cache[(first_word, second_word, third_word)])
                if third_word == end:
                    response.append(first_word)
                    response.append(second_word)
                    break
        
        if response != words:
            for i,name in enumerate(response):
                if name.lower() == "jarvis":
                    response[i] = self.sender.split(' ')[0]
            result = self._untokenize(response)
            
        else:
            random_sent = ["you're not worth talking to.",
                           "talking to you doesn't bring any benefits.",
                           "that's nice.",
                           "i'm not surprised.",
                           "are you sure you can type?",
                           "being honest is a good thing.",
                           "very funny.",
                           "i know a dog with your name",
                           "i have a life of my own to worry about",
                           "i have bigger things on my mind",
                           "are you on something?",
                           "sometimes i don't know whether to laugh at you or pity you."
                            ]
            result = choice(random_sent)
        
        return result

