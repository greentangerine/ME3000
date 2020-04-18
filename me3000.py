#!/usr/bin/env python
from serial import Serial, PARITY_NONE
from umodbus.client.serial import rtu

class ME3000:

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

    INV_STATES = ("WAIT", "CHECK CHARGE", "CHARGE", "CHECK DISCHARGE",
                  "DISCHARGE", "EPS", "FAULT", "PERM FAULT")

    def __init__(self, port, slave):
        self.port_id = port
        self.slave_id = slave
        self.serial_port = self.get_serial_port()


    def get_serial_port(self):
        """ Return serial.Serial instance, ready to use for RS485."""
        port = Serial(port=self.port_id, baudrate=9600, parity=PARITY_NONE,
                      stopbits=1, bytesize=8, timeout=1)
        return port


    def close_serial_port(self):
        self.serial_port.close()


    def set_auto(self):
        """ Switch inverter to AUTO."""
        ret_status = True
        message = rtu.write_passive_register(slave_id=self.slave_id, 
                                             address=self.AUTO, 
                                             value=0)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
          ret_status = False
          response = 0
        return ret_status, response


    def set_charge(self, charge):
        """ Set charge value."""
        ret_status = True
        message = rtu.write_passive_register(slave_id=self.slave_id, 
                                             address=self.CHARGE, 
                                             value=charge)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
            ret_status = False
            response = 0
        return ret_status, response


    def set_discharge(self, discharge):
        """ Set discharge value."""
        ret_status = True
        message = rtu.write_passive_register(slave_id=self.slave_id, 
                                             address=self.DISCHARGE, 
                                             value=discharge)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
            ret_status = False
            response = 0
        return ret_status, response


    def read_holding(self):
        """ Read all the holding registers from inverter."""
        ret_status = True
        message = rtu.read_holding_registers(slave_id=self.slave_id,
                                             starting_address=self.ME_HOLDING, 
                                             quantity=self.NUM_HOLDING)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
            ret_status = False
            response = 0
        return ret_status, response


    def read_input(self):
        """ Read the inverter's input registers."""
        ret_status = True
        message = rtu.read_input_registers(slave_id=self.slave_id,
                                           starting_address=self.ME_INPUT, 
                                           quantity=self.NUM_INPUT)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
            ret_status = False
            response = 0
        return ret_status, response


    def get_inverter_state(self):
        """ Return the inverter state."""
        ret_status = True
        message = rtu.read_holding_registers(slave_id=self.slave_id,
                                             starting_address=self.ME_STATE, 
                                             quantity=1)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
            ret_status = False
            response = [-1]
        return ret_status, response[0], self.INV_STATES[response[0]]


    def get_battery_percentage(self):
        """ Return the current charge percentage of the batteries."""
        ret_status = True
        message = rtu.read_holding_registers(slave_id=self.slave_id,
                                             starting_address=self.BATTPCT,
                                             quantity=1)
        try:
            response = rtu.send_message(message, self.serial_port)
        except:
            ret_status = False
            response = [-1]
        return ret_status, response[0]


