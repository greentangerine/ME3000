#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/pi/ME3000')
from me3000 import ME3000
from datetime import datetime

SLAVE=0x01
SERIAL_PORT="/dev/ttyUSB0"

roo = ME3000(SERIAL_PORT, SLAVE)

print(datetime.now())
print("Get inverter state ...")
status, invstate, invstring = roo.get_inverter_state()
if status:
    print("State = ", invstate, "[", invstring, "]")

print("Get battery percentage ...")
status, response = roo.get_battery_percentage()
if status:
    print(response)

print("Set to auto ...")
retval = -1
while retval < 0:
    status, response = roo.set_auto()
    if status:
        retval = response & 0x00FF
        if retval != 0:
            print("Set auto failed", hex(response))

roo.disconnect()
