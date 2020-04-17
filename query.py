#!/usr/bin/env python
# scripts/example/simple_rtu_client.py

import ME3000 as me

SLAVE=0x01

serial_port = me.get_serial_port()

print("Get all holding registers ...")
status, response = me.read_holding(serial_port, SLAVE)
if status:
  print(response)

print("Get all input registers ...")
status, response = me.read_input(serial_port, SLAVE)
if status:
  print(response)

print("Get inverter state ...")
status, response = me.get_inverter_state(serial_port, SLAVE)
if status:
  print(hex(response))

print("Get battery percentage ...")
status, response = me.get_battery_percentage(serial_port, SLAVE)
if status:
  print(response)

#print("Set to discharge 1000W ...")
#status, response = me.set_discharge(serial_port, SLAVE, 1000)
#print(hex(response))

print("Set to auto ...")
status, response = me.set_auto(serial_port, SLAVE)
if status:
  print(hex(response))

me.close_serial_port(serial_port)
