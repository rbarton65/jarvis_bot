from random import randint, choice
from nltk import word_tokenize
import string
import csv
from ast import literal_eval

class Markov(object):
    
    def __init__(self, text):
        self.text = text
        self.cache = self.get_brain()
        self.words = word_tokenize(text)
        self.word_size = len(self.words)
        self.database()
        
    def get_brain(self):
        with open('markov.csv', 'r') as csv_file:
            spamreader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            responses = {}
            for row in spamreader:
                key, value = literal_eval(row[0]), literal_eval(row[1])
                responses[key] = value
                
            return responses
            
    def write_brain(self):
        with open('markov.csv', 'wt') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for key in self.cache:
                spamwriter.writerow([key, self.cache[key]])
    
    def triples(self):
        '''Creates triples from text, ie "a lovely day" is ("a","lovely","day")'''
        # Check that text is less than 3 words
        if self.word_size < 3:
            return
        
        # Iterate through range of 2 less than amount of words
        for i in range(self.word_size - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])
            
            
    def database(self):
        '''Add text to database'''
        for w1,w2,w3 in self.triples():
            #set tuple as key
            key = (w1, w2)
            print(key)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]
        
        # write to database      
        self.write_brain()  
#        with open('markov.json', 'w') as fp:
#            json.dump(self.cache, fp, sort_keys = True, indent = 4, ensure_ascii=False)

    
    
    def generate_text(self):
        '''Generates text responses'''
        
        stop_words = ['.', '!', '?', ';', ':']
        check_seed = [',','.', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', ':', ';', '"', "'", '?', '/', '>', '<']
        
        # pick a random word from input
        seed = randint(0, self.word_size - 3)
        if self.words[seed] in check_seed:
            generate_text()
        
        seed_word, next_word = self.words[0], self.words[1]
        
        
        # put together response
        response = []
        
        while True:
            response.append(seed_word)
            seed_word, next_word = next_word, choice(self.cache[(seed_word, next_word)])
            if next_word in stop_words:
                response.append(seed_word)
                break
                    
        response.append(next_word)
        result = "".join([" "+i if not i.startswith("'") and not i.startswith("n'") and i not in string.punctuation else i for i in response]).strip()
        result[0].capitalize()
        return result

        
#with open('corpus.txt', 'r') as textfile:
#    result = []
#    for text in textfile:
#        result.append(text)
#    Markov(' '.join(result).replace('\n', ''))
 
text = "my roommate and his girlfriend are trying to make me an okcupid profile..."

message = Markov(text)
print(message.generate_text())