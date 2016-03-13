# -*- coding: utf-8 -*-
import groupy
import math
import random
import string
import re
import wikipedia
import urbandict
import googlemaps
import datetime
import urllib.request
import urllib.parse
import time
import pywapi
import settings
import commands
import nltk
import learn
	
def parse_message(message, bot, messages):
	name = message['name']
	user = message['sender_id']
	text = message['text']
	attach = message['attachments']
	date = message['created_at']
	if text:
		if name == bot.name:
			return
#		elif commands.meg_count(messages):
#			if user == "2994974":
#				bot.post("Shut up, Meg")
#			else:
#				pass
		else:
			print (text)
			if commands.words_in_string(command_list, text.lower()):
				bot.post(commands.cases(commands.words_in_string(command_list, text.lower()).pop(), text.lower(), group))
			elif text.lower() == "ping":
				bot.post("pong")
			elif commands.summary(text):
				bot.post(commands.summary(text))
			elif text.lower() == "jarvis you're a pussy":
				bot.post("What the fuck did you just fucking say about me, you little bitch?")
				time.sleep(4)
				bot.post("I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills.")
				time.sleep(6)
				bot.post("I am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target.")
				time.sleep(5)
				bot.post("I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words.")
				time.sleep(5)
				bot.post("You think you can get away with saying that shit to me over the Internet? Think again, fucker.")
				time.sleep(4)
				bot.post("As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life.")
				time.sleep(6)
				bot.post("You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands.")
				time.sleep(5)
				bot.post("Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit.")
				time.sleep(6)
				bot.post("If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue.")
				time.sleep(5)
				bot.post("But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot.")
				time.sleep(4)
				bot.post("I will shit fury all over you and you will drown in it. You’re fucking dead, %s." % (name.split(' ')[0]))			
			elif "jarvis" in text.lower():
				print ("Name pointed out")
				response = learn.response(text.lower(), learn.import_dictionary())
				bot.post(response)
			else:
				print ("This doesn't concern me")
			
group = settings.jarvis_group
bot = settings.jarvis_bot
members = group.members()
user_greet = ["hello", "howdy", "herro", "hola", "hi", "wingapo", "hey", "yo", "ciao", "ello", "buon giorno", "how are you", "what's up", "whats up", "wassup", "wazzup"]
command_list = ["/info", "/lmgtfy","/google", "/urban", "/map", "/video", "/youtube", "/flip", "/tap", "/current", "/forecast", "/gpoem", "/seen", "/anim"]#, "/help"]
greeting = ["Hello %s!", "It's a pleasure %s", "It's good to see you %s", "Good day %s", "Hi %s", "Greetings %s"]
help = "Hello, I am Jarvis, here are some commands you can use:\n\n/info - research topics\nex: /info {topic}\n\n/lmgtfy,/google - performs a google search\nex: /lmgtfy {topic}\n\n/urban - defines a word from urban dictionary\nex: /urban {word}\n\n/map - estimates travel time between two places\nex: /map from {location} to {location}\n\n/video,/youtube - searches youtube\nex: /video {topic}\n\n/flip - flip a coin!"
bad_words = commands.import_file('/bad_words.txt')

def main(data):
	messages = group.messages()
	parse_message(data, bot, messages)
