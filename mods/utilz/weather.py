import urllib
from xml.dom import minidom

wurl = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
wser = 'http://xml.weather.yahoo.com/ns/rss/1.0'

def weather_for_zip(zip_code):
    global dom
    url = wurl % zip_code +'&u=c'
    dom = minidom.parse(urllib.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(wser, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text')
        })
    ycondition = dom.getElementsByTagNameNS(wser, 'condition')[0]
    return {
        'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'forecasts': forecasts ,
        'title': dom.getElementsByTagName('title')[0].firstChild.data
    }

def toF(c):
    return int((int(c) * (9.0/5.0)) + 32)

def getMsg(zipc):
    a = weather_for_zip(zipc)
    f = a['forecasts']
    msg = 'Currently: High %s, Low %s. %s (%s)' % (toF(f[0]['high']), toF(f[0]['low']), f[0]['condition'], f[0]['date'])
    msg2 = 'Tomorrow: High %s, Low %s. %s (%s)' % (toF(f[1]['high']), toF(f[1]['low']), f[1]['condition'], f[1]['date'])
    return (msg, msg2)