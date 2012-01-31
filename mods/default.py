from example import Cmd, client, RequireAdmin, RequireBotOp, removeCommand
from subprocess import *
import random, sys, os, time
from utilz import weather


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
def opCmd(msg):
	msz = msg.msg.split(' ')
	if len(msz) == 2:
		client.deopUser(msz[1], msg.chan)
	else:
		client.send(msg.chan, 'Usage: '+ deopCmd.usage)

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

@Cmd('!weather', 'Check the weather', '!weather <zipcode>', ['!w'])
def cmdWeather(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		for m in weather.getMsg(msg[1]):
			client.send(obj.chan, m)
	else:
		client.send(obj.chan, 'Usage: '+ cmdWeather.usage)
def init(): pass
