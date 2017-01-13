# Importing everything
from psutil import *
import sys
import time
import datetime
import telepot
import os
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
TGtoken = ConfigSectionMap("Tokens")['telegram']

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
    print "    ##             Carga de CPU:" + str(cpu_pc) + "%. " + " Memoria usada: " + str(virtual_memory().percent) + "%.             ##"
    print "    ########################################################################"
    load = LOAD.create(d_t=str(datetime.datetime.now()), cpu_l='{}%'.format(str(cpu_pc)), ram_l='{}%'.format(str(virtual_memory().percent)), ts_log_stat="Off")
    load.save()

# Terminal cleaning
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main bot loop
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    massa = MSGS.create(msg=command, d_t=str(datetime.datetime.now()), from_who=chat_id)
    massa.save()
    print 'Recibida orden: %s' % command, 'De: %s' % chat_id
    co_list(chat_id, command)

bot = telepot.Bot(TGtoken)
bot.message_loop(handle)

# Function of bot commands
def co_list(chat_id, command):
    mystring = command
    if (mystring.partition(" ")[0] == 'Di'):
        bot.sendMessage(chat_id, mystring.partition(" ")[2])
    if (command == '/ram'):
        bot.sendMessage(chat_id, 'Estoy gastando un {}% de mi RAM.'.format(virtual_memory().percent))
    if (command == '/cpu'):
        bot.sendMessage(chat_id, "Trabajo a un {}% de mi CPU.".format(cpu_percent()))
    if (command == '/hora'):
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    if (command == '/curro'):
        u = round(uppp() / 3600, 1)
        bot.sendMessage(chat_id, 'Ya llevo unas {} horas currando, negrero.'.format(u))

# Startup welcoming and a tick to DB with powerup state
cls()
bottt()
print 'Conexion establecida'
print 'Te escucho, Padre...'
powered = ON.create(power_on_state='OK', d_t=str(datetime.datetime.now()))
powered.save()


while True:
    doit()
    time.sleep(15)