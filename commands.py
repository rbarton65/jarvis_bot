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
import xmltodict
import os
import sys
import giphypop
import pythonUntappd
import foursquare
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())
	
def import_file(file):
	text = open("%s%s" % (os.path.dirname(os.path.realpath(sys.argv[0])), file), 'r')
	result = [line.replace('\n', '') for line in text.readlines()]
	return result

def meg_count(messages):
	meg_count = 0
	for message in messages:
		if message.user_id == "2994974":
			meg_count+=1
	rand = [9,14,24,30,20]
	if meg_count % random.randint(9,13) == 0:
		return True
	else:
		return False

def test_count(messages):
	meg_count = 0
	for message in messages:
		if message.name == "Rich Barton":
			meg_count+=1
	rand = [9,14,24,30,20]
	if meg_count % random.randint(9,13) == 0:
		return True
	else:
		return False

def info_search(text):
	keyword = "/info "
	search = text.split(keyword, 1)[1]
	try:	
		result = ("%s - %s" % (wikipedia.summary(search, sentences=2), wikipedia.page(search).url))
		return result
	except:
		result = ('"%s" does not match any pages. Try again!"' % (search.capitalize()))
		return result
	
def lmgtfy(text):
	keyword = "/lmgtfy "
	try:
		search = text.split(keyword, 1)[1]
	except:
		search = text.split("/google ", 1)[1]
	lmgtfy = search.replace(' ', '+')
	result = ("http://lmgtfy.com/?q=%s" % (lmgtfy))
	return result
	
def urban(text):
	keyword = "/urban "
	search = text.split(keyword, 1)[1]
	try:
		word = urbandict.define('%s' % search)[0]['word'].replace('\n', '').capitalize()
		definition = urbandict.define('%s' % search)[0]['def']
		example = urbandict.define('%s' % search)[0]['example']
		result = ("%s\n\nDefinition:\n%s\n\nExamples:\n%s" % (word,definition,example))
		return result
	except:
		result = ("Could not look up%s, sorry about that." % search.capitalize())
		return result

def map(text):
	gmaps = googlemaps.Client(key=settings.gmaps_key)
	r = re.compile('from(.*?)to')
	keyword = "to "
	m = r.search(text)
	if m:
		start = m.group(1)
	else:
		result = ('Please follow the template "/map from {location} to {location}"')
		return result
	destination = text.split(keyword, 1)[1]
	now = datetime.datetime.now()
	directions_result = gmaps.directions(start, destination, mode="driving", departure_time=now)
	duration = directions_result[0]['legs'][0]['duration']['text']
	start_address = directions_result[0]['legs'][0]['start_address']
	end_address = directions_result[0]['legs'][0]['end_address']
	distance = directions_result[0]['legs'][0]['distance']['text']
	result = ("Right now, it would take %s to drive %s from %s to %s." % (duration, distance, start_address, end_address))
	return result
	
def youtube(text):
	keyword = "/video "
	try:
		query_string = urllib.parse.urlencode({"search_query" : text.split(keyword, 1)[1]})
	except:
		query_string = urllib.parse.urlencode({"search_query" : text.split("/youtube ", 1)[1]})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	result = ("http://www.youtube.com/watch?v=" + search_results[0])
	return result

def flip(text):
	coin = random.randint(0,1)
	if coin == 0:
		result = ("Tails")
	else:
		result = ("Heads")
	return result
		
def get_current_weather(text):
	keyword = "/current "
	location = text.split(keyword, 1)[1]
	try:
		id = list(dict.keys(pywapi.get_location_ids(location)))[0]
		w = pywapi.get_weather_from_yahoo(id, 'imperial')
		temp = "%s\u00b0F" % (w['condition']['temp'])
		loc = "%s, %s" % (w['location']['city'], w['location']['region'])
		status = w['condition']['text'].lower()
		result = "Current conditions show %s, %s in %s" % (status, temp, loc)
		return result
		
	except:
		try:
			id = location
			w = pywapi.get_weather_from_yahoo(id, 'imperial')
			temp = "%s\u00b0F" % (w['condition']['temp'])
			loc = "%s, %s" % (w['location']['city'], w['location']['region'])
			status = w['condition']['text'].lower()
			result = "Current conditions show %s, %s in %s" % (status, temp, loc)
			return result
		except:
			result = ("Please enter valid location or zip code.")
			return result

def get_forecast_weather(text):
	keyword = "/forecast "
	location = text.split(keyword, 1)[1]
	try:
		id = list(dict.keys(pywapi.get_location_ids(location)))[0]
		w = pywapi.get_weather_from_yahoo(id, 'imperial')
		forecast = []
		for i in w['forecasts']:
			low = "%s\u00b0F" % (i['low'])
			high = "%s\u00b0F" % (i['high'])
			status = i['text']
			day = i['day']
			forecast.append("%s: H:%s L:%s - %s" % (day, high, low, status))	
		weather = "5 Day Forecast for %s, %s\n\n" % (w['location']['city'], w['location']['region'])
		weather += '\n'.join(forecast)
		result = (weather)
		return result
		
	except:
		try:
			id = location
			w = pywapi.get_weather_from_yahoo(id, 'imperial')
			forecast = []
			for i in w['forecasts']:
				low = "%s\u00b0F" % (i['low'])
				high = "%s\u00b0F" % (i['high'])
				status = i['text']
				day = i['day']
				forecast.append("%s: H:%s L:%s - %s" % (day, high, low, status))	
			weather = "5 Day Forecast for %s, %s\n\n" % (w['location']['city'], w['location']['region'])
			weather += '\n'.join(forecast)
			result = (weather)
			return result
		except:
			result = ("Please enter valid location or zip code.")
			return result

def gpoem(text):
	keyword = "topic "
	try:
		search = text.split(keyword, 1)[1].replace('"', '')
	except:
		return "Please follow the template '/gpoem topic {topic}'"
	poem = search.replace(' ', '+')
	url = "http://www.google.com/complete/search?output=toolbar&q=%s" % (poem)
	response = urllib.request.urlopen(url)
	data = response.read()
	doc = xmltodict.parse(data)
	poem_list = []
	try:
		for i in range(0,len(doc['toplevel']['CompleteSuggestion'])):
			poem_list.append(doc['toplevel']['CompleteSuggestion'][i]['suggestion']['@data'])
		random.shuffle(poem_list)
		poem = "\n".join(poem_list[0:4])
		return '"%s" - a short poem\n\n%s' % (search.title(), poem)
	except:
		return "My apologies, I couldn't make a poem out of that topic."

def seen(text, group):
	keyword = "/seen "
	name = text.split(keyword, 1)[1]
	messages = group.messages()
	mem = 0
	for i in group.members():
		if name.lower() in i.nickname.lower():
			mem = 1
			break
	if mem == 1:
		pass
	elif name.lower().replace('.', '') == "jarvis":
		return "I am omnipresent."
	else:
		return "'%s' isn't a name in this group chat." % (name)
	found = 0
	for i in messages:
		if name.lower() in i.name.lower():
			format = "%Y-%m-%d %H:%M:%S"
			pref = "%b %d, %Y at %I:%M%p"
			s = i.created_at.strftime(pref)
			result = "%s was last seen on %s." % (i.name, s)
			found = 1
			break

	if found == 0:	
		print ("This might take a bit...")
		try:
			while messages.iolder():
				pass
		except:
			pass
		for i in messages:
			if name.lower() in i.name.lower():
				format = "%Y-%m-%d %H:%M:%S"
				pref = "%b %d, %Y at %I:%M%p"
				s = i.created_at.strftime(pref)
				result = "%s was last seen on %s." % (i.name, s)
				break
			else:
				result = "I was not able to find %s." % name.capitalize()		
	return result

def summary(text):
	LANGUAGE = "english"
	SENTENCES_COUNT = 2
	url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
	blacklist = import_file('/blacklist.txt')
	if url:
		if words_in_string(blacklist, re.sub('[^a-zA-Z0-9\n\.]', ' ', url)):
			return
		else:
			parser = HtmlParser.from_url(url[0], Tokenizer(LANGUAGE))
			stemmer = Stemmer(LANGUAGE)
			summarizer = Summarizer(stemmer)
			summarizer.stop_words = get_stop_words(LANGUAGE)
			summary = []
			for sentence in summarizer(parser.document, SENTENCES_COUNT):
				summary.append(str(sentence))
			return "Too Long, Didn't Read Summary:\n\n%s" % "\n\n".join(summary)
	else:
		return

def anim(text):
	keyword = "/anim "
	search = text.split(keyword, 1)[1]
	try:
		g = giphypop.Giphy()
		img = g.translate(search)
		return img.media_url
	except:
		return "I was not able to find a gif explaining your feelings."
		
def tap(text):
	r = re.compile('at (.*?) in')
	keyword = "in "
	m = r.search(text)
	if m:
		bar = m.group(1)
	else:
		result = ('Please follow the template "/tap at {bar} in {location}"')
		return result
	location = text.split(keyword, 1)[1]
	untappd_api = pythonUntappd.api(settings.untappd_id,settings.untappd_secret)
	untappd_api.set_auth(settings.untapped_key)
	foursquare_api = foursquare.Foursquare(client_id=settings.foursquare_id, client_secret=settings.foursquare_secret)
	foursquare_api.set_access_token(settings.fourquare_key)
	try:
		four_venue = foursquare_api.venues.search(params={'query': '%s' % bar, 'near' : '%s' % location})
	except:
		return "That location isn't searchable."
	four_id = four_venue['venues'][0]['id']
	try:
		untappd_id = untappd_api.foursquare_venue_lookup(four_id)['response']['venue']['items'][0]['venue_id']
	except:
		return "I'm sorry, I cannot find that bar."
	venue = untappd_api.venue_info(str(untappd_id))
	top_beers = []
	try:
		for i in range(5):
			top_beers.append(venue['response']['venue']['top_beers']['items'][i])

		info = "Top beers at %s (%s, %s, %s):\n" % (venue['response']['venue']['venue_name'], venue['response']['venue']['location']['venue_address'], venue['response']['venue']['location']['venue_city'], venue['response']['venue']['location']['venue_state'])
		result = [info]
		for i in top_beers:
			result.append('\n"%s" by %s (%s @ %s%%)' % (i['beer']['beer_name'], i['brewery']['brewery_name'], i['beer']['beer_style'], i['beer']['beer_abv']))
			
		return ''.join(result)
	except:
		return "Sadly there's no data for that bar."

def cases(command, text, group):
	switcher = {
		'/info': info_search,
		'/lmgtfy': lmgtfy,
		'/google': lmgtfy,
		'/urban': urban,
		'/map': map,
		'/video': youtube,
		'/youtube': youtube,
		'/flip': flip,
		'/current': get_current_weather,
		'/forecast': get_forecast_weather,
		'/gpoem': gpoem,
		'/seen': seen,
		'/anim': anim,
		'/tap': tap,
#		'/help': help
	}
	func = switcher.get(command)
	try:
		return func(text)
	except:
		return func(text, group)


#print(cases('/info world'))
