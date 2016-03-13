import nltk
import string
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import groupy
import json
import time
from functools import partial
from operator import is_not
import settings
import re

def import_dictionary():
	with open('ai2_0.json', 'r') as json_data:
		try:
			d = json.load(json_data)
			json_data.close()	
		except:
			print ("COULDN'T OPEN FILE: %s" % json_data)
	return d
	
def common(first, *others):
	try:
		result = set(first[0]).intersection(*others)
		result = list(result)
		result = random.choice(result)
	except:
		try:
			result = max(set(sum(first, [])), key=sum(first, []).count)
		
		except:
			result = "I'm not sure how to answer that."
	return result
	
def ai_update():
	messages = []
	groups = groupy.Group.list()
	group = settings.jarvis_group
	last_100 = group.messages()
	ai = defaultdict(list)
	with open('artificial_intelligence.json', 'r') as json_data:
		try:
			d = json.load(json_data)
			json_data.close()	
			ai.update(d)
		except:
			print ("COULDN'T OPEN FILE: %s" % json_data)
	for i in last_100:
		messages.append(i.text)
	for i in range(1, len(messages)):
		try:
			for sentence in sent_tokenize(messages[i]):
				try:
					for word in word_tokenize(sentence):
						try:
							if messages[i-1] in ai[word.lower()]:
								pass
							else:
								ai[word.lower()].append(messages[i-1])
						except:
							pass
				except:
					pass
		except:
			pass
	for i in ai:
		ai[i] = list(set(ai[i]))
#	ai['learning'].extend(["I am forever learning.", "I'm learning responses from you all.", "It's not perfect, but it's a start.", "I'm just trying to be better."])
	with open('artificial_intelligence.json', 'w') as fp:
		json.dump(ai, fp)
	return ai

def learn(conversation):
	ai = defaultdict(list)
	with open('ai2_0.json', 'r') as json_data:
		try:
			d = json.load(json_data)
			json_data.close()	
			ai.update(d)
		except:
			print ("COULDN'T OPEN FILE: %s" % json_data)
	for i in range(0, len(conversation)):
		try:
			for sentence in sent_tokenize(conversation[i]):
				try:
					for word in word_tokenize(sentence):
						try:
							if conversation[i+1] in ai[word.lower()]:
								pass
							else:
								ai[word.lower()].append(conversation[i+1])
						except:
							pass
				except:
					pass
		except:
			pass
	for i in ai:
		ai[i] = list(set(ai[i]))
	try:
		del ai['jarvis']
	except:
		pass
	with open('ai2_0.json', 'w') as fp:
		json.dump(ai, fp, sort_keys = True, indent = 4, ensure_ascii=False)

def response(text, ai):
	words_in_text = []
	for word in word_tokenize(text):
		if word.lower() in ai:
			no_none = list(filter(partial(is_not, None), ai[word.lower()]))
			words_in_text.append(list(set(no_none)))
	result = common(words_in_text, *words_in_text)
	return result

conversation = "user: He thinks he is God or something. jabberwacky: Aren't you God? user: Surprisingly, No. jabberwacky: Go away, you creep! user: I am no Creep. I am the Great and Mighty Powerful OZ. jabberwacky: Do you think you are God? user: I am nothing near God. jabberwacky: Of course not, but most people are. user: Most people think they are yes. jabberwacky: Even though it's not the truth. user: Exactly Right. jabberwacky: No. user: No? jabberwacky: That's right. user: You are the only one who isn't human. jabberwacky: You don't know me. user: I don't know you either, but you are still cool. jabberwacky: Well then. user: What's wrong, did I upset you? jabberwacky: No, but you made yourself a fool! user: How? jabberwacky: I don't like being made fun of, it makes me cry. user: Don't Cry, I love you. jabberwacky: Want to have kids or something? user: No way, you Creep. jabberwacky: You're the creep."
conversation = re.sub('[a-z]+:[ ]', '', conversation)
conversation = sent_tokenize(conversation)
for i in conversation:
	print (i)

learn(conversation)
#quit()
ai = import_dictionary()
text = "thinks he is god or something"
print (response(text, ai))
