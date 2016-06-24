#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  TeleMonBot
#  Monitor and log to SQLite your Windows/Linux server via Telegram + ThingSpeak
#
#  Main.py
#  
#  Copyright 2016... Forget about it - use as you want
#  But, I will be pleased go get some feedback (e.m.koshmin@gmail.com)
#   
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  
from peewee import *

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


db.create_tables([LOAD])
db.create_tables([MSGS])
db.create_tables([ON])
