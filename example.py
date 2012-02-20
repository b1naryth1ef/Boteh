from irclib import Connection, Client, Listener
import cPickle as pickle
import thread, time, sys, os

version = 0.2
mods = ['default', 'dj', 'github', 'logger']
modfiles = []
Listener = Listener
FILE = None

threads = []
aliass = {}
commands = {}
matchers = {}
savez = {}
adys = ['B1|Irssi', 'B1|Phone', 'B1naryTh1ef']

def loadSave():
	global FILE, savez
	if os.path.exists('save_file.dat'):
		FILE = open('save_file.dat', 'rw')
		savez = pickle.load(FILE)
	else:
		open('save_file.dat', 'w').close()
		FILE = open('save_file.dat', 'rw')
	
def appendSave(tag, obj):
	savez[tag] = obj

def dumpSave():
	global savez, FILE
	pickle.dump(savez, FILE)

@Listener('chansay')
@Listener('privsay')
def matcher(obj):
	if matchers != {}:
		matching(obj)

def matching(line):
	for i in matchers.keys():
		if i in line.msg.lower():
			threads.append(thread.start_new_thread(matchers[i], (line,)))

def rmvCmd(command):
	if command in commands.keys():
		del commands[command]
	if command in aliass.keys():
		del aliass[command]

def removeCommand(command):
	if type(command) in (list, tuple):
		for i in command:
			rmvCmd(i)
	else: rmvCmd(command)

class Command():
	def __init__(self, cmd, exe, desc, usage, alias):
		self.cmd = cmd
		self.desc = desc
		self.usage = usage
		self.alias = alias
		self.exe = exe

		for i in self.alias:
			aliass[i] = cmd

def Cmd(cmd, desc, usage, alias=[]):
	def deco(func):
		commands[cmd] = Command(cmd, func, desc, usage, alias)
		func.usage = usage
		func.description = desc
		func.command = cmd
		func.rmv = [i for i in alias]
		func.rmv.append(cmd)
		return func
	return deco

def Match(textlist):
	def deco(func):
		for text in textlist:
			matchers[text] = func
		return func
	return deco

def RequireAdmin(func):
	def deco(msg):
		if client.isClientAdmin(msg.nick):
			return func(msg)
		else:
			return client.sendMustBeAdmin(msg.chan)
	return deco

def RequireBotOp(func):
	def deco(msg):
		if client.isClientOp(msg.chan):
			return func(msg)
		else:
			return client.sendClientMustBeOp(msg.chan)
	return deco

@Listener('command')
def cmdParser(obj):
	i = obj.msg.split(' ')[0]
	print 'Command Fire: %s' % i
	if i in commands:
		threads.append(thread.start_new_thread(commands[i].exe, (obj,)))
	elif i in aliass:
		threads.append(thread.start_new_thread(commands[aliass[i]].exe, (obj,)))

@Listener('join')
def cmdParser(obj):
	if obj.nick == client.nick:
		time.sleep(2) #Wait to get NICKS message
		for admin in adys:
		 	print admin, client.makeAdmin(admin)
		if client.isClientOp(obj.chan):
			for chan in client.channels.values():
			 	if admin in chan.users.keys() and client.isClientAdmin(admin):
			 		client.opUser(admin)
	elif client.users[obj.nick].admin is True:
		client.opUser(obj.nick, obj.chan)
	elif obj.nick in adys:
		client.makeAdmin(adys)
		if client.isClientOp():
			client.opUser(obj.nick)

def loop():
	while True:
		if client.alive is False: break
		client.parse(conn.recv())

def init():
	global conn, client

	conn = Connection(network='irc.quakenet.org', nick='BroMan').startup()
	client = Client(conn)
	client.joinChannel('#bitchnipples')
	client.botMode = True

	loadSave()

	for i in mods:
		__import__('mods.'+i)
		try:
			i = sys.modules['mods.'+i]
			threads.append(thread.start_new_thread(i.init, ()))
		except Exception, e:
			print 'MODULE ERROR: Please add the function init() to your module.[', e, ']'
	loop()

if __name__ == '__main__':
	print 'Please start using the command "python start.py"'
