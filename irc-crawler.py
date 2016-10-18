#!/usr/bin/python

###############################################
# Exercice : Crawl irc and avoid being banned #
###############################################

import irc.bot 
import irc.client
from pymongo import MongoClient

from time import sleep
from datetime import datetime
import random
import re

#---[ td;dr ]------------------------------
# 1. Connect to mongodb
# 2. Generate nickname + realname from wordlist
# 3. Connect to irc server + join chan
# 4. Say hello
# 5. Log host, port, chan, sender info, time, 
#    connected users into db for each message

#---[ parameters ]-------------------------
host = "irc.example.net"
port = 6667
chan = "#chan"
nick = ""
real = ""

#---[ db setup ]---------------------------
db_addr = "127.0.0.1"
database = "test-db"
collection = "irclogger"
client = MongoClient(db_addr)
db = client[database]
coll = db[collection]

#---[ wordlists & msg ]--------------------------
with open('./answers.wordlist','r') as a:
    answers = a.readlines()
with open('./nicknames.wordlist','r') as n:
    nicklist = n.readlines()
with open('./realnames.wordlist','r') as r:
    reallist = r.readlines()
welcomemsg = "Hi everyone :)"

#---[ main ]-------------------------------
def main():
    gen_names()
    irccrawler().start()

#---[ fill db ]----------------------------
def send_to_db(dbnick,dbreal,msg,users):
    coll.insert_one({
        "host": host,
        "port": port,
        "chan": chan,
        "sender-nickname": dbnick,
        "sender-realname": dbreal,
        "message": msg,
        "time": datetime.utcnow(),
        "connected-users": users
    })

#---[ avoid ban ]--------------------------
def gen_names():
    global nick
    global real
    nick = random.choice(nicklist) + random.choice(nicklist)
    real = random.choice(reallist)
    nick = re.sub('\W+','', nick)
    real = re.sub('\W+','', real)

# + auto-answer in "on_privmsg" events

#---[ irc bot ]----------------------------
class irccrawler(irc.bot.SingleServerIRCBot):
    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [(host,port)], nick, real)

    # When connected to server, join chan and send hello message
    def on_welcome(self, serv, ev):
        serv.join(chan)
        sleep(2)
        serv.privmsg(chan, welcomemsg)

    # When message is posted on chan, log all
    def on_pubmsg(self, serv, ev):
        conusers = ""
        message = ev.arguments[0]
        sendernick = ev.source.nick
        senderreal = ev.source.user
        target = ev.target
        conusers = " ".join([user.encode('utf-8') for user in
            self.channels[target].users()])
        send_to_db(sendernick,senderreal,message,conusers)

    # Answer to private message
    def on_privmsg(self, serv, ev):
        sendernick = ev.source.nick
        sleep(random.randint(1,3))
        serv.privmsg(sendernick, random.choice(answers).strip('\r').strip('\n'))


if __name__ == '__main__':
    main()

