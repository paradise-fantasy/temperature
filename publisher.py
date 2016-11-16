#!/usr/bin/python

import urllib2
import paho.mqtt.publish as publish
import subprocess, json
from time import sleep
import random

avoid_spam = 0
url_get_present = "http://api.komstek.no/api/presence?limit=1&sort=-_arrivedAt"
url_get_members = "http://api.komstek.no/api/users"

members = json.loads(urllib2.urlopen(url_get_members).read())
paradiseMembers = map(lambda x: x["name"], filter(lambda x: x["room"] == "paradise", members))


def getTemp(script):
    proc = subprocess.Popen("/home/pi/temperature/" + script, stdout=subprocess.PIPE, shell=True)
    (temp, error) = proc.communicate()
    return temp

def sendTemp():
    global avoid_spam
    inside = float(getTemp('inside.sh'))/1000
    print(inside)
    insideTemp = {'sensor': 'Inside', 'temperature': inside}
    outside = float(getTemp('outside.sh'))/1000
    outsideTemp = {'sensor': 'Outside', 'temperature': outside}
    publish.single("paradise/api/temperature", json.dumps(insideTemp), port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
    publish.single("paradise/api/temperature", json.dumps(outsideTemp), port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
    if (inside > 24):
        if (avoid_spam<=0):
            avoid_spam = 15
            someone = getSomeonePresent()
            if someone:
                response =  "It is getting hot in here, " + someone + " please take off all your clothes!"
                publish.single("paradise/notify/tts", response, port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")

        else:
            avoid_spam-=1
    else:
        avoid_spam=0
    sleep(5)

def getSomeonePresent():
    peoplePresent = urllib2.urlopen(url_get_present).read()
    peoplePresent = json.loads(peoplePresent)[0]["_value"]["status"]
    paradisePresent = []
    for person in peoplePresent:
        name = person.keys()[0]
        if name in paradiseMembers and person[name]:
            paradisePresent.append(name)
    if len(paradisePresent) == 0:
        return 0
    return random.choice(paradisePresent)


#print (getTemp('inside.sh'))
while True:
    sendTemp()
