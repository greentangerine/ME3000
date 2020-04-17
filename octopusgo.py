#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/pi/ME3000')
import ME3000 as me
from datetime import datetime

SLAVE=0x01
THRESHOLD_FILE="/home/pi/ME3000/pct.txt"

print(datetime.now())

try:
    tfile = open(THRESHOLD_FILE, "r")
    threshold = int(tfile.readline().split("=")[-1])
    if (threshold < 20) or (threshold > 100):
        threshold = 100
except:
    # default to fully charged
    threshold = 100

serial_port = me.get_serial_port()

print("Charge threshold =", threshold)
print("Get inverter state ...")
status, invstate, invstring = me.get_inverter_state(serial_port, SLAVE)
if status:
    print("State = ", invstate, "[", invstring, "]")

print("Get battery percentage ...")
status, response = me.get_battery_percentage(serial_port, SLAVE)
if status:
    print(response)
    if response < threshold:
        print("Below threshold, set to charge 3000W ...")
        status, response = me.set_charge(serial_port, SLAVE, 3000)
        if status:
            retval = response & 0x00FF
            if retval != 0:
                print("Set charge failed ...")
    elif invstate == 2:
        print("Over threshold and charging, so switch to auto ...")
        status, response = me.set_auto(serial_port, SLAVE)
        if status:
            retval = response & 0x00FF
            if retval != 0:
                print("Set auto failed", hex(response))

me.close_serial_port(serial_port)
