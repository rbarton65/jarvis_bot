from random import randint, choice

class Markov(object):
    
    cache = {}
    
    def __init__(self, text):
        self.text = text
        self.words = self.text.split()
        self.word_size = len(self.words)
        self.database()
        
    
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
                self.cache[key] = w3
        print(self.cache)
    
    
    def generate_text(self, size = 25):
        
        seed = randint(0, self.word_size - 3)
        print(seed)
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        print(seed_word, next_word)
        response = []
        
        for i in range(size):
            response.append(seed_word)
            seed_word, next_word = next_word, choice(self.cache[(seed_word, next_word)])
        
        response.append(next_word)
        return ' '.join(response)
        

text = "My aunt has a self playing piano in her dining room that is operated by remote control. She has it set so that it can play the theme song from Michael Myers at the touch of a button, and that's her plan for if someone breaks in late at night."

message = Markov(text)
print(message.generate_text())