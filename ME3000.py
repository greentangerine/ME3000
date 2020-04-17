#!/usr/bin/env python
from serial import Serial, PARITY_NONE
from umodbus.client.serial import rtu

# some constants from the Passive protocol
DISCHARGE=0x0101
CHARGE=0x0102
AUTO=0x0103

ME_HOLDING=0x0200 
NUM_HOLDING=69
# specific holding registers
ME_STATE=0x0200
BATTPCT=0x0210

ME_INPUT=0x10B0 
NUM_INPUT=13

INV_STATES = ("WAIT", "CHECK CHARGE", "CHARGE", "CHECK DISCHARGE", "DISCHARGE",
              "EPS", "FAULT", "PERM FAULT")

# define some useful functions

def get_serial_port():
    """ Return serial.Serial instance, ready to use for RS485."""
    port = Serial(port='/dev/ttyUSB0', baudrate=9600, parity=PARITY_NONE,
                  stopbits=1, bytesize=8, timeout=1)
    return port


def close_serial_port(serial_port):
    serial_port.close()


def set_auto(serial_port, slave):
    """ Switch inverter to AUTO."""
    ret_status = True
    message = rtu.write_passive_register(slave_id=slave, 
                                         address=AUTO, 
                                         value=0)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = 0
    return ret_status, response


def set_charge(serial_port, slave, charge):
    """ Set charge value."""
    ret_status = True
    message = rtu.write_passive_register(slave_id=slave, 
                                         address=CHARGE, 
                                         value=charge)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = 0
    return ret_status, response


def set_discharge(serial_port, slave, discharge):
    """ Set discharge value."""
    ret_status = True
    message = rtu.write_passive_register(slave_id=slave, 
                                         address=DISCHARGE, 
                                         value=discharge)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = 0
    return ret_status, response


def read_holding(serial_port, slave):
    """ Read all the holding registers from inverter."""
    ret_status = True
    message = rtu.read_holding_registers(slave_id=slave,
                                         starting_address=ME_HOLDING, 
                                         quantity=NUM_HOLDING)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = 0
    return ret_status, response


def read_input(serial_port, slave):
    """ Read the inverter's input registers."""
    ret_status = True
    message = rtu.read_input_registers(slave_id=slave,
                                       starting_address=ME_INPUT, 
                                       quantity=NUM_INPUT)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = 0
    return ret_status, response


def get_inverter_state(serial_port, slave):
    """ Return the inverter state."""
    ret_status = True
    message = rtu.read_holding_registers(slave_id=slave,
                                         starting_address=ME_STATE, 
                                         quantity=1)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = [-1]
    return ret_status, response[0], INV_STATES[response[0]]


def get_battery_percentage(serial_port, slave):
    """ Return the current charge percentage of the batteries."""
    ret_status = True
    message = rtu.read_holding_registers(slave_id=slave,
                                         starting_address=BATTPCT,
                                         quantity=1)
    try:
        response = rtu.send_message(message, serial_port)
    except:
        ret_status = False
        response = [-1]
    return ret_status, response[0]


