#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/pi/ME3000')

from me3000 import ME3000
from MyME3000 import *

roo = ME3000(SERIAL_PORT, SLAVE)

print("Get all holding registers ...")
status, response = roo.read_holding()
if status:
    print(response)

print("Get all input registers ...")
status, response = roo.read_input()
if status:
    print(response)

print("Get inverter state ...")
status, invstate, invstring = roo.get_inverter_state()
if status:
    print("State = ", invstate, "[", invstring, "]")

print("Get battery percentage ...")
status, response = roo.get_battery_percentage()
if status:
  print(response)

print("Set standby ...")
status, response = roo.set_standby()
if status:
    retval = hex(response & 0x00FF)
    print(retval)

print("Set auto ...")
status, response = roo.set_auto()
if status:
    retval = hex(response & 0x00FF)
    print(retval)


roo.disconnect()
