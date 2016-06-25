# Importing everything
from psutil import *
import sys
import time
import datetime
import telepot
import os
import random
import httplib, urllib
from PyQt4.QtGui import *
from uptime import uptime as uppp
from peewee import *
import ConfigParser

# Connecting config
Config = ConfigParser.ConfigParser()
Config.read('config.ini')
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
global TGtoken
global TStoken
TGtoken = ConfigSectionMap("Tokens")['telegram']
TStoken = ConfigSectionMap("Tokens")['thingspeak']

# Connecting database
db = SqliteDatabase('botdb.db')
class MSGS(Model):
    msg = CharField()
    d_t = CharField()
    from_who = CharField()

    class Meta:
        database = db
class ON(Model):
    power_on_state = CharField()
    d_t = CharField()
    class Meta:
        database = db
class LOAD(Model):
    d_t = CharField()
    cpu_l = CharField()
    ram_l = CharField()
    ts_log_stat = CharField()
    class Meta:
        database = db
db.connect()

# Global variables
last_worktime = 0
last_idletime = 0
global command
global bash
global globrand
global status
global reason

# Logo:)
def bottt():
    print "    ########################################################################"
    print "    #  __  __             _ _             _               ____        _    #"
    print "    # |  \/  |           (_) |           (_)             |  _ \      | |   #"
    print "    # | \  / | ___  _ __  _| |_ ___  _ __ _ _ __   __ _  | |_) | ___ | |_  #"
    print "    # | |\/| |/ _ \| '_ \| | __/ _ \| '__| | '_ \ / _` | |  _ < / _ \| __| #"
    print "    # | |  | | (_) | | | | | || (_) | |  | | | | | (_| | | |_) | (_) | |_  #"
    print "    # |_|  |_|\___/|_| |_|_|\__\___/|_|  |_|_| |_|\__, | |____/ \___/ \__| #"
    print "    #                                              __/ |                   #"
    print "    #                                             |___/                    #"
    print "    ########################################################################"
    print "    #              Created by E_KOsh (e.m.koshmin@gmail.com).              #"
    print "    ########################################################################"

# Main monitoring function
def doit():
    cpu_pc = cpu_percent()
    cls()
    bottt()
    print "    ##             Cpu load is: " + str(cpu_pc) + "%. " + "Memory load is: " + str(
        virtual_memory().percent) + "%.             ##"
    print "    ########################################################################"
    if sys.argv == 'TS':
        ts(cpu_pc, meme)
    else:
        status = 'Logging'
        reason = 'Disabled'
    load = LOAD.create(d_t=str(datetime.datetime.now()), cpu_l='{}%'.format(str(cpu_pc)), ram_l='{}%'.format(str(virtual_memory().percent)),
                       ts_log_stat="Logged to TS. Answer is: {} and that's {}".format(str(status), str(reason)))
    load.save()

# ThingSpeak function, called by doit(), if you runned the code with 'TS' argument
def ts(cpu_pc, meme):
    params = urllib.urlencode({'field1': cpu_pc, 'field2': meme, 'key': TStoken})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    responsee = [(response.status, response.reason)]
    for (status, reason) in responsee:
        print "    ##             Logged to TS. Answer is: {} and that's {}             ##".format(str(status),
                                                                                                   str(reason))
    print "    ########################################################################"
    data = response.read()
    conn.close()

# Terminal cleaning
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main bot loop
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    massa = MSGS.create(msg=command, d_t=str(datetime.datetime.now()), from_who=chat_id)
    massa.save()
    print 'Got a command: %s' % command, 'From: %s' % chat_id
    globrand = random.randint(0, 10)
    co_list(chat_id, command, globrand)

bot = telepot.Bot(TGtoken)
bot.message_loop(handle)

# Function of bot commands
def co_list(chat_id, command, globrand):
    if (command == 'Where are you?'):
        import geocoder
        import urllib
        url = 'http://myexternalip.com/raw'
        bot.sendLocation(chat_id, geocoder.ip(urllib.urlopen(url).read()).latlng[0], geocoder.ip(urllib.urlopen(url).read()).latlng[1])
    mystring = command
    if (mystring.partition(" ")[0] == 'Say,'):
        vari = mystring.partition(" ")[2]
        if globrand <= 5:
            bot.sendMessage(chat_id, vari.rpartition('or')[0])
        else:
            bot.sendMessage(chat_id, vari.rpartition('or')[2])
    if (command == 'Where are you all?'):
        bot.sendMessage(chat_id, 'I am here!')
    if (command == 'Screenshot'):
        app = QApplication(sys.argv)
        QPixmap.grabWindow(QApplication.desktop().winId()).save('screenshot.jpg', 'jpg')
        bot.sendPhoto(chat_id, open('screenshot.jpg', 'rb'))
    if (command == 'RAM usage'):
        bot.sendMessage(chat_id, 'Nearly {}% of RAM is used.'.format(virtual_memory().percent))
    if (command == 'Who is your creator?'):
        bot.sendMessage(chat_id, 'His nick is E_KOsh...')
        bot.sendMessage(chat_id, "You might want to write him... Don't be so shy - @E_KOsh")
    if (command == 'CPU usage'):
        bot.sendMessage(chat_id, "About {}% of my CPU power is used.".format(cpu_percent()))
    if (command == 'What is the time?'):
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    if (command == 'Uptime'):
        u = round(uppp() / 3600, 1)
        bot.sendMessage(chat_id, 'I am already working for {} hours.'.format(u))

# Startup welcoming and a tick to DB with powerup state
cls()
bottt()
print 'Connection established'
print 'I am listening, Father...'
powered = ON.create(power_on_state='OK', d_t=str(datetime.datetime.now()))
powered.save()


while True:
    doit()
    time.sleep(15)