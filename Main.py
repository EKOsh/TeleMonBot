#!/usr/bin/python
# -*- coding: utf-8 -*-

#Поставь все эти библиотеки через PIP
#Install all these libraries via PIP
#<pip install *имя библиотеки/library name*>

from psutil import *
import sys
import time
import datetime
import telepot
import os
import random
import httplib, urllib
from PIL import Image
from PyQt4.QtGui import *
from PyQt4 import *
from PIL import *
import ctypes
from uptime import uptime as uppp
import xlsxwriter
from peewee import *

global TGtoken
global TStoken
TGtoken = 'Enter your Telegram token here / Вставь сюда свой токен телеграма'
TStoken = 'Enter your ThingSpeak write token here / Вставь сюда свой код доступа к ThingSpeak'


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

#После первого запуска закомментируй эти 3 строчки
#Comment these 3 rows after the first start
db.create_tables([LOAD])
db.create_tables([MSGS])
db.create_tables([ON])


last_worktime = 0
last_idletime = 0

global command
global bash
global globrand


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


def memory_usage_resource():
    mem = virtual_memory()
    return mem.percent


def doit():
    cpu_pc = cpu_percent()
    meme = memory_usage_resource()
    params = urllib.urlencode({'field1': cpu_pc, 'field2': meme, 'key': TStoken})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    responsee = [(response.status, response.reason)]
    cls()
    bottt()
    # print "    ########################################################################"
    print "    ##              Cpu load is: " + str(cpu_pc) + "%. " + "Memory load is: " + str(
        meme) + "%.              ##"
    print "    ########################################################################"
    for (status, reason) in responsee:
        print "    ##             Logged to TS. Answer is: {} and that's {}             ##".format(str(status),
                                                                                                   str(reason))
    print "    ########################################################################"
    load = LOAD.create(d_t=str(datetime.datetime.now()), cpu_l='{}%'.format(str(cpu_pc)), ram_l='{}%'.format(str(meme)),
                       ts_log_stat="Logged to TS. Answer is: {} and that's {}".format(str(status), str(reason)))
    load.save()
    data = response.read()
    conn.close()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def loca(chat_id, command):
    if command == 'Where are you?':
        import geocoder
        import urllib
        url = 'http://myexternalip.com/raw'
        bot.sendLocation(chat_id, geocoder.ip(urllib.urlopen(url).read()).latlng[0],
                         geocoder.ip(urllib.urlopen(url).read()).latlng[1])


def resolvator(chat_id, command, globrand):
    mystring = command
    if mystring.partition(" ")[0] == 'Say, ':
        vari = mystring.partition(" ")[2]
        if globrand <= 5:
            bot.sendMessage(chat_id, vari.rpartition('or')[0])
        else:
            bot.sendMessage(chat_id, vari.rpartition('or')[2])


def screen(chat_id):
    app = QApplication(sys.argv)
    QPixmap.grabWindow(QApplication.desktop().winId()).save('screenshot.jpg', 'jpg')
    bot.sendPhoto(chat_id, open('screenshot.jpg', 'rb'))


def say(chat_id, command):
    mytuple = command.partition(" ")
    if mytuple[0] == 'Say: ':
        bot.sendMessage(chat_id, mytuple[2])


def pere(chat_id, command):
    if command == 'Where are you all?':
        bot.sendMessage(chat_id, 'I am here!')


def screenmsg(chat_id, command):
    if command == 'Screenshot':
        screen(chat_id)


def rampd(chat_id, command):
    if command == 'RAM usage'
        bot.sendMessage(chat_id, 'Nearly {}% of RAM is used.'.format(memory_usage_resource()))


def daddypd(chat_id, command):
    if command == 'Who is your creator?'
        bot.sendMessage(chat_id, 'His nick is E_KOsh...')
        bot.sendMessage(chat_id, "You might want to write him... Don't be so shy - @E_KOsh")


def cpupd(chat_id, command):
    if (command == 'CPU usage'
        bot.sendMessage(chat_id, "About {}% of my CPU power is used.".format(cpu_percent()))


def ostimepd(chat_id, command):
    if command == 'What is the time?'
        bot.sendMessage(chat_id, str(datetime.datetime.now()))


def uptimepd(chat_id, command):
    if command == 'Uptime'
        u = round(uppp() / 3600, 1)
        bot.sendMessage(chat_id, 'I am already working for {} hours.'.format(u))


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    massa = MSGS.create(msg=command, d_t=str(datetime.datetime.now()), from_who=chat_id)
    massa.save()
    print 'Got a command: %s' % command, 'From: %s' % chat_id
    globrand = random.randint(0, 10)
    daddypd(chat_id, command)
    cpupd(chat_id, command)
    ostimepd(chat_id, command)
    uptimepd(chat_id, command)
    rampd(chat_id, command)
    screenmsg(chat_id, command)
    pere(chat_id, command)
    say(chat_id, command)
    resolvator(chat_id, command, globrand)
    loca(chat_id, command)
    loggg(chat_id, command)


bot = telepot.Bot(TGtoken)
bot.message_loop(handle)
cls()
bottt()
print 'Connection established'
print 'I am listening, Father...'
powered = ON.create(power_on_state='OK', d_t=str(datetime.datetime.now()))
powered.save()


while True:
    doit()
    time.sleep(15)
