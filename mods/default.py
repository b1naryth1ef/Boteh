from example import Cmd, client, RequireAdmin, RequireBotOp, removeCommand, Listener, Match
from subprocess import *
from utilz import weather
import random, sys, os, time, json, urllib, example

chan_topics = {}
warns = {}
listens = {}
maxwarn = 3
warntime = 5*60 #in seconds

trans = {
	True:'On',
	False:'Off'
}

match_hilist = ['hello',
'hi',
'sup',
'heya',
'hey',
'heyo',
'hay']

lovelist = ['I cannot compute love...',
'from love import hug; hug()',
'ily2',
'you really love me?',
'<3']

hilist = ['Well hello to you too!',
'Hows it going?',
'Wazup good sir!',
'HEYO!',
'Waz cookin?',
'YOU SAID HI!!!! <3']

byelist = ["I'm gonna go party somewhere else...", 
'Peace YO!', 
'Gotta go tell Neek to stop having such loud sex.', 
'lmfao brb ttylijos', 
'I wonder what this button does...', 
'Fonducci what are you doing? NO WAIT DONT TOUCH TH-', 
"Java? Oh lemme just killl myself then...",
'from main import FuckYouGuys',
'class Neek(OldMan.Balls): return lame',
'while Afro: print "racist"',
"G'BYE YOU NUBSERS!",
'LOLLY! DONT POINT THAT GUN TH-',
'Time to go trololololing in bot heaven',
'Can\' touch this!']

@Match(['<3', 'ily'])
def matchLove(obj):
	if obj.msg.startswith(client.nick):
		client.send(obj.chan, '%s: %s' % (obj.nick, random.choice(lovelist)))

@Match(match_hilist)
def matchHello(obj):
	if obj.msg.startswith(client.nick):
		client.send(obj.chan, '%s: %s' % (obj.nick, random.choice(hilist)))

@Cmd('!uptime', 'List uptime of the box', '!uptime', ['!up'])
def cmdUptime(obj):
	msg = obj.msg.split(' ')
	p = Popen(["uptime"], stdout=PIPE, close_fds=True)
	up = p.stdout.readline().strip().split(' ', 1)
	client.send(obj.chan, 'Uptime: '+str(up[1:][0]))

@Cmd('!version', 'Print-out the latest version of the bot (from the git header).', '!version', ['!ver'])
def version(msg):
	p = Popen(["git", "log", "-n 1"], stdout=PIPE, close_fds=True)
	commit = p.stdout.readline()
	author = p.stdout.readline()
	date = p.stdout.readline()
	#client.send(msg.chan, 'Version: '+str(api.getVersion()))
	client.send(msg.chan, "Git: "+commit)
	client.send(msg.chan, author)
	client.send(msg.chan, date)

@Cmd('!quit', 'Nicely exit irc.', '!quit [goodbye message]', ['!q'])
@RequireAdmin
def quit(msg):
	#!quit blah blah blah
	msgz = msg.msg.split(' ', 1)
	cli = msg.nick
	save()
	if len(msgz) == 1:
		client.quit(random.choice(byelist))
	elif len(msgz) == 2:
		client.quit(msgz[1])
	sys.exit() #For now

@Cmd('!1337', 'For testing usage only!', '!1337', ['!l33t'])
def l33t(msg):
	client.makeAdmin(msg.nick)
	client.send(msg.chan, 'Enjoy your l33tness!')
	removeCommand(l33t.rmv)

@Cmd('!opme', 'You\'ve been good! Take an OP!', '!opme')
@RequireAdmin
@RequireBotOp
def opmeCmd(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 1:
		client.opUser(msg.nick, msg.chan)
		client.send(msg.chan, '%s: Well hello there you sexy beast! About time you had OP...' % msg.nick)
	else:
		client.send(msg.chan, 'Usage: '+ opmeCmd.usage)

@Cmd('!op', 'Op a user', '!op <user>')
@RequireAdmin
@RequireBotOp
def opCmd(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		client.opUser(msz[1], msg.chan)
	else:
		client.send(msg.chan, 'Usage: '+ opCmd.usage)

@Cmd('!deop', 'Deop a user', '!deop <user>')
@RequireAdmin
@RequireBotOp
def deopCmd(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		client.deopUser(msz[1], msg.chan)
	else:
		client.send(msg.chan, 'Usage: '+ deopCmd.usage)

@Cmd('!voice', 'Voice a user', '!voice <user>')
@RequireAdmin
@RequireBotOp
def voiceCmd(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		client.voiceUser(msz[1], msg.chan)
	else:
		client.send(msg.chan, 'Usage: '+ voiceCmd.usage)

@Cmd('!devoice', 'Devoice a user', '!devoice <user>')
@RequireAdmin
@RequireBotOp
def devoiceCmd(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		client.devoiceUser(msz[1], msg.chan)
	else:
		client.send(msg.chan, 'Usage: '+ devoiceCmd.usage)

@Cmd('!addadmin', 'Add an admin.', '!addadmin <user>')
@RequireAdmin
def addAdmin(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		if client.makeAdmin(msz[1]): client.send(msg.chan, 'Added %s as an admin' % msz[1])
		else: client.send(msg.chan, 'Unknown user %s' % msz[1])
	else: client.send(msg.chan, 'Usage: '+ addAdmin.usage)

@Cmd('!rmvadmin', 'Remove an admin.', '!rmvadmin <user>')
@RequireAdmin
def rmvAdmin(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		if client.removeAdmin(msz[1]): client.send(msg.chan, 'Removed %s as an admin' % msz[1])
		else: client.send(msg.chan, 'Unknown user %s' % msz[1])
	else: client.send(msg.chan, 'Usage: '+ rmvAdmin.usage)

@Cmd('!join', 'Join a channel.', '!join <channel>')
@RequireAdmin
def joinChan(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		if not client.isClientInChannel(msz[1]):
			client.joinChannel(msz[1])
			client.send(msg.chan, 'Joined channel %s' % msz[1])
		else: client.send(msg.chan, 'Can\'t is already in %s.' % msz[1])
	else: client.send(msg.chan, 'Usage: '+ joinChan.usage)

@Cmd('!part', 'Part (leave) a channel', '!part <channel> [msg]')
@RequireAdmin
def partChan(msg):
	msz = msg.msg.split(' ')
	if len(msz) in [2,3]:
		if len(msz) == 3: m = msz[2]
		else: m = random.choice(byelist)
		if client.isClientInChannel(msz[1]):
			client.partChannel(msz[1], m)
			client.send(msg.chan, 'Parted channel %s' % msz[1])
		else: client.send(msg.chan, 'Can\'t part channel %s, not in it.' % msz[1])
	else: client.send(msg.chan, 'Usage: '+ partChan.usage)

@Cmd('!kick', 'Kick a user from the channel', '!kick <user> [reason] (must be sent from channel)', ['!k'])
@RequireAdmin
@RequireBotOp
def cmdKick(obj):
	msg = obj.msg.split(' ', 2)
	if len(msg) == 2 and obj.chan != client.nick:
		client.sendRaw('KICK %s %s' % (obj.chan, msg[1]))
		client.send(msg.chan, 'Kicked %s from %s.' % (msg[1], obj.chan))
	elif len(msg) == 3 and obj.chan != client.nick:
		client.sendRaw('KICK %s %s :%s' % (obj.chan, msg[1], msg[2]))
		client.send(msg.chan, 'Kicked %s from %s for %s.' % (msg[1], obj.chan, msg[2]))
	else:
		client.send(msg.chan, 'Usage: '+ cmdKick.usage)

# @Cmd('!tempban', 'Temporarily ban a user from the channel', '!tempban <user>', ['!tb'])
# @RequireAdmin
# @RequireBotOp
# def cmdTempBan(obj):
# 	print 'Winning!'

@Cmd('!ban', 'Ban a user from the channel', '!ban <user/*banmask>', ['!b'])
@RequireAdmin
@RequireBotOp
def cmdBan(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		if msg[1].startswith('*'): banmask = msg[1][1:]
		else: banmask = msg[1]
		client.sendRaw('MODE %s +b %s' % (obj.chan, banmask))
	else:
		client.send(obj.chan, 'Usage: '+ cmdBan.usage)

@Cmd('!topic', 'Set the topic of a channel', '!topic <topic>')
@RequireBotOp
@RequireAdmin
def cmdTopic(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		client.sendRaw('TOPIC %s :%s' % (obj.chan, msg[1]))
	else:
		client.send(obj.chan, 'Usage: '+ cmdTopic.usage)

@Cmd('!shout', 'Shout to one or more channels', '!shout <[*]channel/all> <message>', ['!!'])
@RequireAdmin
def cmdShout(obj):
	msg = obj.msg.split(' ', 2)
	if len(msg) == 3:
		msgz = msg[2]
		if msg[1] == 'all':
			for i in client.channels.keys():
				client.send(i, msgz)
		elif msg[1].startswith('*'):
			client.joinChannel(msg[1][1:])
			time.sleep(1)
			client.send(msg[1][1:], msgz)
			time.sleep(1)
			client.partChannel(msg[1][1:])
		elif client.isClientInChannel(msg[1]):
			client.send(msg[1], msgz)
		else:
			client.send(obj.chan, 'Not in channel %s. To join/send/part append * to the channel (!shout *#blah msg)' % msg[1])
	else:
		client.send(obj.chan, 'Usage: '+ cmdShout.usage)

@Cmd('!time', 'Check the time/date', '!time', ['!date'])
def cmdTime(obj):
	client.send(obj.chan, 'Time: %s' % time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))

@Cmd('!weather', 'Check the weather', '!weather <zipcode>', ['!temp'])
def cmdWeather(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		for m in weather.getMsg(msg[1]):
			client.send(obj.chan, m)
	else:
		client.send(obj.chan, 'Usage: '+ cmdWeather.usage)

@Cmd('!warn', 'Warn a user after they misbehave!', '!warn <user> [reason]', ['!w'])
@RequireAdmin
@RequireBotOp
def cmdWarn(obj):
	msg = obj.msg.split(' ', 2)
	if len(msg) >= 2:
		if len(msg) == 2: reason = 'Your behavior is not respective to the desired environment.'
		elif len(msg) == 3: reason = msg[2]
		if msg[1] in warns and client.channels[obj.chan].hasUser(msg[1]):
			warns[msg[1]][0] += 1
			if warns[msg[1]][0] >= maxwarn:
				client.send(msg[1], 'You\'ve been kicked for having too many warnings! Please rejoin after %s seconds!' % (warntime))
				client.sendRaw('KICK %s %s :%s' % (obj.chan, msg[1], 'Too many warnings!'))
				warns[msg[1]][1] = time.time()+warntime
			else:
				client.send(obj.chan, '%s: Warning %s of %s: %s' % (msg[1], warns[msg[1]][0], maxwarn, reason))
		elif client.channels[obj.chan].hasUser(msg[1]):
			warns[msg[1]] = [1, None]
			client.send(obj.chan, '%s: Warning %s of %s: %s' % (msg[1], warns[msg[1]][0], maxwarn, reason))
	else:
		client.send(obj.chan, 'Usage: '+cmdWarn.usage)

@Cmd('!clear', 'Clear a user of warnings!', '!clear <user>', ['!c'])
@RequireAdmin
def cmdClear(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		if msg[1] in warns.keys():
			del warns[msg[1]]
			client.send(obj.chan, 'User %s cleared of all warnings.' % msg[1])
		else:
			client.send(obj.chan, 'User %s has not been warned.' % msg[1])
	else:
		client.send(obj.chan, 'Usage: '+cmdClear.usage)

@Cmd('!help', 'View all commands, or info on an individual command.', '!help [command]')
def cmdHelp(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		if msg[1] in example.commands.keys():
			c = example.commands[msg[1]]
			client.send(obj.nick, 'Command %s: %s. Usage: %s.' % (msg[1], c.desc, c.usage))
		else:
			client.send(obj.nick, 'Unknown command %s. List all commands with !help.' % msg[1])
	else:
		if obj.nick != obj.chan and client.isClientInChannel(obj.chan):
 			client.send(obj.chan, '%s: sending you a list of commands...' % obj.nick) 
		line = []
		first = True
		for cmd in example.commands.keys():
			if first is True:
					first = False
					line = ['Commands: %s' % cmd]
			elif len(line) >= 10:
				client.send(obj.nick, ', '.join(line))
				line = [cmd]
			else:
				line.append(cmd)
		client.send(obj.nick, ', '.join(line))

@Cmd('!google', 'Google something', '!google <term>', ['!g'])
def cmdGoogle(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		amount = 3
		BASE_URL = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
		url = BASE_URL + urllib.urlencode({'q' : msg[1].encode('utf-8').strip()})
		raw_res = urllib.urlopen(url).read()
		results = json.loads(raw_res)
		m = []
		for x,i in enumerate(results['responseData']['results']):
			if x > 3: break
			m.append(' - '.join((urllib.unquote(i['url']), i['titleNoFormatting'])))
		client.send(obj.chan, 'Top 3 Results for %s:' % msg[1])
		for i in m:
			client.send(obj.chan, i)
	else:
		client.send(obj.chan, 'Usage: '+cmdGoogle.usage)

@Cmd('!tt', 'Dynamicall control the topic', '"!tt help" for info', ['!topictools'])
@RequireAdmin
def cmdTopicTools(obj):
	global chan_topics
	#!tt topic lalalala
	#!tt +suffix prefix append
	#!tt -suffix suffix append
	#!tt lock
	def sep(inp):
		if inp == '' or inp == ' ': return ''
		else: return ' | '

	msg = obj.msg.split(' ', 2)
	if obj.chan not in chan_topics:
		chan_topics[obj.chan] = {
						'prefix':'',
						'suffix':'',
						'topic':'',
						'format':'',
						'locked':False}

	topic = chan_topics[obj.chan]

	if len(msg) == 3:
		if msg[1].startswith('-') or msg[1].startswith('+'): 
			df = msg[1][:1]
			cd = msg[1][1:]
		else: 
			df = ''
			cd = msg[1]
		if msg[2] == '*': msg[2] = ''
		if cd == 'prefix':
			if df == '': topic['prefix'] = msg[2]
			elif df == '-': topic['prefix'] = topic['prefix']+msg[2]
			elif df == '+': topic['prefix'] = msg[2]+topic['prefix']
		elif cd == 'suffix':
			if df == '': topic['suffix'] = msg[2]
			elif df == '-': topic['suffix'] = topic['suffix']+msg[2]
			elif df == '+': topic['suffix'] = msg[2]+topic['suffix']
		elif cd == 'topic':
			if df == '': topic['topic'] = msg[2]
			elif df == '-': topic['topic'] = topic['topic']+msg[2]
			elif df == '+': topic['topic'] = msg[2]+topic['topic']
		# elif cd == 'format':
		# 	if msg[2].count('%s') == 3:
		# 		topic['foramt'] = msg[2]
		# 	else:
		# 		client.send(obj.chan, 'Format must have 3 %s\'s in it')
		else: return None #Unkown command
		top = '%s%s%s%s%s' % (topic['prefix'], sep(topic['topic']), topic['topic'], sep(topic['suffix']),topic['suffix'])
		client.sendRaw('TOPIC %s :%s' % (obj.chan, top))
	elif len(msg) == 2:
		if msg[1] == 'help':
			client.send(obj.chan, 'Help, Lock (Toggle lock). Topic, Suffix, Prefix with modifiers +[Append] -[Suffixify]. Example: !tt +suffix Add To Front Of Suffix')
		elif msg[1] == 'lock':
			topic['locked'] = not topic['locked']
			client.send(obj.chan, 'Topic is now %s' % trans[topic['locked']])

@Listener('join')
def warnListen(obj):
	if obj.nick in warns.keys():
		if warns[obj.nick][1] != None:
			if time.time()-warns[obj.nick][1] >= 0:
				del warns[obj.nick]
			else:
				client.sendRaw('KICK %s %s :%s' % (obj.chan, obj.nick, 'You\'re warning has not expired! You have %s more seconds to go!' % abs(time.time()-warns[obj.nick][1])))

@Listener('topic')
def topicListen(obj):
	if obj.chan in chan_topics:
		if chan_topics[obj.chan]['locked'] is True:
			topic = chan_topics[obj.chan]
			top = '%s%s%s' % (topic['prefix'], topic['topic'], topic['suffix'])
			client.sendRaw('TOPIC %s :%s' % (obj.chan, top))

def save():
	if example.useStorage:
		example.saveObj('chan_topics', {})

def init():
	if example.useStorage:
		if example.hasObj('chan_topics'):
			chan_topics = example.loadObj('chan_topics')
		else:
			save()
