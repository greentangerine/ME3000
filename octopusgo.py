#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/pi/ME3000')
from me3000 import ME3000
from datetime import datetime
from MyME3000 import *

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
        charge_rate = 3000 # todo - maybe vary charge rate
        
        print("Below threshold, set to charge at", charge_rate)
        status, response = roo.set_charge(charge_rate)
        if status:
            retval = response & 0x00FF
            if retval != 0:
                print("Set charge failed ...")
    elif invstate == 2 or invstate == 0:
        print("Over threshold and charged, so switch to auto ...")
        status, response = roo.set_auto()
        if status:
            retval = response & 0x00FF
            if retval != 0:
                print("Set auto failed", hex(response))

roo.disconnect()
