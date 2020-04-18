#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/pi/ME3000')
from me3000 import ME3000
from datetime import datetime

SLAVE=0x01
THRESHOLD_FILE="/home/pi/ME3000/pct.txt"
SERIAL_PORT="/dev/ttyUSB0"

print(datetime.now())

try:
    tfile = open(THRESHOLD_FILE, "r")
    threshold = int(tfile.readline().split("=")[-1])
    if (threshold < 20) or (threshold > 100):
        threshold = 100
except:
    # default to fully charged
    threshold = 100

roo = ME3000(SERIAL_PORT, SLAVE)


print("Charge threshold =", threshold)
print("Get inverter state ...")
status, invstate, invstring = roo.get_inverter_state()
if status:
    print("State = ", invstate, "[", invstring, "]")

print("Get battery percentage ...")
status, response = roo.get_battery_percentage()
if status:
    print(response)
    if response < threshold:
        print("Below threshold, set to charge 3000W ...")
        status, response = roo.set_charge(3000)
        if status:
            retval = response & 0x00FF
            if retval != 0:
                print("Set charge failed ...")
    elif invstate == 2:
        print("Over threshold and charging, so switch to auto ...")
        status, response = roo.set_auto()
        if status:
            retval = response & 0x00FF
            if retval != 0:
                print("Set auto failed", hex(response))

roo.close_serial_port()
