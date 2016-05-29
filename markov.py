from random import randint, choice
from nltk import word_tokenize
import string
import json

class Markov(object):
    
    def __init__(self, text):
        self.text = text
        self.cache = self.get_brain()
        self.words = word_tokenize(text)
        self.word_size = len(self.words)
        self.database()
        
    def get_brain(self):
        with open('markov.json', 'r') as json_data:
            try:
                d = json.load(json_data)
                json_data.close()	
                return d
            except:
                print ("COULDN'T OPEN FILE: %s" % json_data)
                return {}

    
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
        with open('markov.json', 'w') as fp:
            json.dump(self.cache, fp, sort_keys = True, indent = 4, ensure_ascii=False)

    
    
    def generate_text(self):
        '''Generates text responses'''
        
        stop_words = ['.', '!', '?']
        check_seed = [',','.', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', ':', ';', '"', "'", '?', '/', '>', '<']
        
        # pick a random word from input
        seed = randint(0, self.word_size - 3)
        if self.words[seed] in check_seed:
            generate_text()
        
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        
        
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
        return result.capitalize()

        

text = "First off, my thanks to all those lovely people that replied to my original thread. I never expected so many comments for my fairly insignificant issue. Anyway. I went ahead and did it. Monday evening, it was just the two of us at my place, pretty much like any other night when he slept over. Except when I 'accidentally' had my phone slip from my hand and got off the couch to get it so that I could get on one knee and propose to Peter. He was at a loss for words. Then he started laughing. Then he left the room for a second while I was looking confused, still on one knee and with the ring in my hand. When he came back, he got down on the floor with me and asked me the same thing, with a ring in his hand! I don't doubt we looked very silly when we both started laughing. Then we tried to put the rings on each other's fingers at the same time, which led to some more silly shit, but all in all, it was great. Apparently, he'd been carrying the ring with him for the past five months. He wanted to originally propose for New Years eve, but didn't manage to get the ring in time, so he waited for another shot at it. The rest of the evening went perfect! Yeah, we had to throw out the food left on the table in the morning, but hey, the night before was totally worth it! I waited until Wednesday, so we could both get out the news to our families and friends that we were now officially engaged to be married, before I hit him up with my gift. We talked a lot on it, and eventually he asked me to for a few days to process it, as it was a fairly big deal to answer to in the moment. I made sure that he knew that I didn't give a damn about whether he got the degree or not, and if he wanted, I could give him a full language course as an alternative gift, or even for us to travel and stay abroad for several months so he could immerse himself in another language completely. We were spending the night over at his place yesterday and he gave me his answer regarding the gift. While he was really, really appreciative to the lengths I'd go to help him fulfill one of his dreams from his youth, he said that ultimately it was just something of a passing fancy back then and even now, with all the expenses paid for, he didn't really want it or need it. One of the primary reasons why he didn't want to go and officially study at a university is that he thought that would probably prove taxing on our relationship and he didn't want that. Studying another language is all neat and good, but not at the expense of the life we've built together or the life we would have in the future. The language course idea was also neat, he said, but in the end he thinks it would be more enjoyable for the both of us if we took that extended trip abroad. That said, I don't think we'll be doing all that much for learning the lagnuage. Mind you, won't bother me none. So that's it then, folks. No 4 years of studying, no delays on the wedding. Come this winter, Peter will be my husband and I'll be his wife! God, my head's still up in the clouds and there's a part of me that can't really believe this is happening. I've never been more happy! To all the galls and fellas from the previous thread, again, my thanks!"

message = Markov(text)
print(message.generate_text())