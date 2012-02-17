from example import Cmd, client, RequireAdmin, RequireBotOp, removeCommand, Listener
import logging
import logging.handlers
import os

togglez = {
'on':True,
'off':False,
}

chans = {}
enabled = False
web = True

@Cmd('!log', 'Check the log status, enable/disable.', '!log [on/off]')
@RequireAdmin
def cmdLog(obj):
	global enabled
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		if msg[1] in togglez:
			enabled = togglez[msg[1]]
			client.send(obj.chan, 'Logging is now %s.' % msg[1])
		else:
			client.send(obj.chan, 'Invalid value for logging toggle! (on/off)')
	elif len(msg) == 1:
		client.send(obj.chan, 'Logging is %s' % [i for i in togglez.keys() if togglez[i] == enabled][0])
	else:
		client.send(obj.chan, 'Usage: '+cmdLog.usage)

@Cmd('!logchan', 'Add a channel to the log', '!logchan <channel>')
@RequireAdmin
def cmdLogChan(obj):
	msg = obj.msg.split(' ', 1)
	if len(msg) == 2:
		if msg[1] not in chans and client.isClientInChannel(msg[1]):
			handle = logging.FileHandler('./logs/%s.log' % msg[1])
			handle.setFormatter('%(asctime)s %(message)s')
			chans[msg[1]] = [logging.getLogger(msg[1]), open('./logs/%s.log' % msg[1])]
			chans[msg[1]][0].addHandler(handle)

@Listener('chansay')
def listenz(obj):
	if enabled is True:
		if obj.chan in chans.keys():
			chans[obj.chan][0].info('%s: %s' % (obj.nick, obj.msg))

def init():
	global app
	if 'logs' not in os.listdir(os.getcwd()):
		os.mkdir('logs')
	logging.basicConfig(level='INFO', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	for i in client.channels.keys():
		handle = logging.FileHandler('./logs/%s.log' % i) #logging.handlers.RotatingFileHandler('%s.log' % i, mode='a')
		handle.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
		chans[i] = [logging.getLogger(i), open('./logs/%s.log' % i)]
		chans[i][0].addHandler(handle)