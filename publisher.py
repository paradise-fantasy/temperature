#!/usr/bin/python

import paho.mqtt.publish as publish
import subprocess, json
from time import sleep

def getTemp(script):
    proc = subprocess.Popen("/home/pi/temperature/" + script, stdout=subprocess.PIPE, shell=True)
    (temp, error) = proc.communicate()
    return temp

def sendTemp():
    inside = float(getTemp('inside.sh'))/1000
    print(inside)
    insideTemp = {'sensor': 'Inside', 'temperature': inside}
    outside = float(getTemp('outside.sh'))/1000
    outsideTemp = {'sensor': 'Outside', 'temperature': outside}
    publish.single("paradise/api/temperature", json.dumps(insideTemp), port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
    publish.single("paradise/api/temperature", json.dumps(outsideTemp), port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
    sleep(2.5)

#print (getTemp('inside.sh'))
while True:
    sendTemp()
