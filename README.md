# TeleMonBot
Monitor and log to SQLite your Windows/Linux server via Telegram + ThingSpeak (freaky, yep?)

Python 2,7 script

Used python libraries: psutil, telepot, PyQt4 and peewee

The code is really raw right now... But, well, you can use it and tell me about your experience. My telegram is @E_KOsh. Email e.m.koshmin@gmail.com

For read before sleep: www.thingspeak.com/ www.telegram.org/ 

Huge THANKS to GitHub user Nick Lee! Check out his project www.github.com/nickoala/telepot


## Installation (Linux):

Clone my code to your lovely linux pc:

$  git clone https://github.com/EKOsh/TeleMonBot TeleMonBot && cd TeleMonBot

Install all libs + SQLite DB browser and create a DB for future logging:

$  sudo chmod +x inst.sh && sudo ./inst.sh

Now, open the config.ini file with any editor, paste your telegram bot api code and thingspeak channel write code (I think you got them while your before_sleep_readind) and save+close it

Are you excited? Let’s run it!

$  sudo python Main.py

## If everything is OK, you will get your terminal look like this:

![Terminal](https://github.com/EKOsh/TeleMonBot/blob/master/terminal.png)

[Telegram][www.telegram.org/]
[ThingSpeak][www.thingspeak.com/]


