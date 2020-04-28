#!/usr/bin/env python3

# me3000_mqtt.py

import paho.mqtt.client as mqtt
import time
import numpy
import struct
import sys
sys.path.insert(0, '/home/pi/ME3000')
from me3000 import ME3000
from MyME3000 import *

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True 
        #print("connected OK Returned code=", rc)
        #client.subscribe(topic)
    else:
        print("Bad connection Returned code= ",rc)
        client.bad_connection_flag = True

roo = ME3000(SERIAL_PORT, SLAVE)

status, me3000_response = roo.read_holding()
if status != True:
    print("Read failed: exiting ...")
    roo.disconnect()
    quit()

mqtt.Client.bad_connection_flag = False
mqtt.Client.connected_flag = False

client = mqtt.Client(ME3000_NAME)
client.on_connect = on_connect
client.loop_start()
client.username_pw_set(MQTT_USER, MQTT_PWD)
client.connect(MQTT_HOST)

while not client.connected_flag and not client.bad_connection_flag:
    time.sleep(1)

if client.bad_connection_flag:
    client.loop_stop()
    print("MQTT connection failed ...")
    quit()

# just upload the selected values in TOPICS
# List of (index in holding registers, name for feed, signed/unsigned 16-bit)

for topic in TOPICS:
    t_value = me3000_response[topic[0]]
    if topic[2] == 'h': # using struct.pack format
        t_value = numpy.int16(t_value) # convert to signed
    t_value = int(t_value) # ensure int - need this for some reason
    t_topic = 'emon/me3000/' + topic[1] # build topic name
    ret = client.publish(t_topic, t_value)
    if ret[0] != 0:
       print("Publish failed for" + t_topic)

client.disconnect()
roo.disconnect()
