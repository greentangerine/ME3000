#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/pi/ME3000')
import ME3000 as me
from datetime import datetime

SLAVE=0x01

serial_port = me.get_serial_port()

print(datetime.now())
print("Get inverter state ...")
status, invstate, invstring = me.get_inverter_state(serial_port, SLAVE)
if status:
    print("State = ", invstate, "[", invstring, "]")

print("Get battery percentage ...")
status, response = me.get_battery_percentage(serial_port, SLAVE)
if status:
    print(response)

print("Set to auto ...")
retval = -1
while retval < 0:
    status, response = me.set_auto(serial_port, SLAVE)
    if status:
        retval = response & 0x00FF
        if retval != 0:
            print("Set auto failed", hex(response))

me.close_serial_port(serial_port)
