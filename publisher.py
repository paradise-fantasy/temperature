#!/usr/bin/python

import paho.mqtt.publish as publish
import subprocess, json
from time import sleep

avoid_spam = 0

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
            avoid_spam = 5
            publish.single("paradise/notify/tts", "it is gettin hot in here, so take of all your clothes!", port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
        else:
            avoid_spam-=1
    else:
        avoid_spam=0
    sleep(5)

#print (getTemp('inside.sh'))
while True:
    sendTemp()
