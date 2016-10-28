#!/usr/bin/python

import paho.mqtt.publish as publish
import subprocess, json
from time import sleep

def getTemp():
    proc = subprocess.Popen('/home/pi/1-wire_temp.sh', stdout=subprocess.PIPE, shell=True)
    (temp, error) = proc.communicate()
    print temp
    return temp

val = float(getTemp())/1000

temperature = {'sensor': '1-wire', 'temperature': val}

publish.single("paradise/api/temperature", json.dumps(temperature), port=8883, tls={'ca_certs':"/home/pi/ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
sleep(2.5)
