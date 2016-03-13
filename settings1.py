import groupy

def get_group(id):
	groups = groupy.Group.list()
	for i in groups:
		if i.group_id == id:
			group = i
	return group

def get_bot(id):
	bots = groupy.Bot.list()
	for i in bots:
		if i.bot_id == id:
			bot = i
	return bot

gmaps_key=''
rt_key = ''
untappd_id = ''
untappd_secret = ''
untapped_key = ''
foursquare_id = ''
foursquare_secret = ''
fourquare_key = ''
jarvis_group = get_group("")
jarvis_bot = get_bot("")
