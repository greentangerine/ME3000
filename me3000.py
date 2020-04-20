#!/usr/bin/env python
import struct
from serial import Serial, PARITY_NONE
from umodbus.client.serial import rtu
from umodbus.functions import function_code_to_function_map, ModbusFunction


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

    port_id = None
    slave_id = None
    serial_port = None

    def __init__(self, port, slave):
        self.port_id = port
        self.slave_id = slave
        self.serial_port = self.get_serial_port()


    def connect(self):
        if self.serial_port is not None:
            self.serial_port = self.get_serial_port()


    def get_serial_port(self):
        """ Return serial.Serial instance, ready to use for RS485."""
        port = Serial(port=self.port_id, baudrate=9600, parity=PARITY_NONE,
                      stopbits=1, bytesize=8, timeout=1)
        return port


    def disconnect(self):
        if self.serial_port is not None:
          self.close_serial_port()


    def close_serial_port(self):
        self.serial_port.close()
        self.serial_port = None


    def set_auto(self):
        """ Switch inverter to AUTO."""
        ret_status = True
        message = write_passive_register(slave_id=self.slave_id, 
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
        message = write_passive_register(slave_id=self.slave_id, 
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
        message = write_passive_register(slave_id=self.slave_id, 
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


def write_passive_register(slave_id, address, value):
    """ Return ADU for Modbus extended function code 66: Write Passive Register.

    :param slave_id: Number of slave.
    :return: Byte array with ADU.
    """
    function = WritePassiveRegister()
    function._address = address
    function._value = value

    return rtu._create_request_adu(slave_id, function.request_pdu)

# SoFar ME30000 Passive Mode
WRITE_PASSIVE_REGISTER = 66



class WritePassiveRegister(ModbusFunction):
    """ Implement SoFar Modbus function code 66.

        This function code is used to write a single holding register in a
        remote device. 
        The Request PDU specifies the address of the register to
        be written. 
        The response is consists of the slave id, function code, byte count
        and status bytes.

    The request PDU with function code 66 must be 5 bytes:

        ================ ===============
        Field            Length (bytes)
        ================ ===============
        Function code    1
        Address          2
        Value            2
        ================ ===============

    The PDU can unpacked to this:

    ..
        Note: the backslash in the bytes below are escaped using an extra back
        slash. Without escaping the bytes aren't printed correctly in the HTML
        output of this docs.

        To work with the bytes in Python you need to remove the escape sequences.
        `b'\\x01\\x00d` -> `b\x01\x00d`

    .. code-block:: python

        >>> struct.unpack('>BHh', b'\\x42\\x00d\\x00\\x03')
        (6, 100, 3)

    The reponse PDU is a two byte status value.

        ================ ===============
        Field            Length (bytes)
        ================ ===============
        Function code    1
        Byte Count       1
        Status Value     2
        ================ ===============

    """
    function_code = WRITE_PASSIVE_REGISTER

    _address = None
    _count = 2
    _value = None
    data = None

    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        """ Value to be written on register.

        :param value: An integer.
        :raises: IllegalDataValueError when value isn't in range.
        """
        try:
            struct.pack('>h', value)
        except struct.error:
            raise IllegalDataValueError

        self._value = value


    @property
    def request_pdu(self):
        """ Build request PDU to write single register.

        :return: Byte array of 5 bytes with PDU.
        """
        if None in [self._address, self._value]:
            # TODO Raise proper exception.
            raise Exception

        return struct.pack('>BHh', self.function_code,
                           self._address, self._value)


    @staticmethod
    def create_from_request_pdu(pdu):
        """ Create instance from request PDU.

        :param pdu: A request PDU.
        """
        _, address, value = \
            struct.unpack('>BHh', pdu)

        instance = WritePassiveRegister()
        instance._address = address
        instance._value = value

        return instance


    @property
    def expected_response_pdu_size(self):
        """ Return number of bytes expected for response PDU.

        :return: number of bytes.
        """
        return 4


    def create_response_pdu(self):
        fmt = '>BBH'
        ret_val = struct.pack(fmt, 
                              self.function_code, self._count, self.data)
        return ret_val


    @staticmethod
    def create_from_response_pdu(resp_pdu):
        """ Create instance from response PDU.

        :param resp_pdu: Byte array with request PDU.
        :return: Instance of :class:`WritePassiveRegister`.
        """
        write_passive_register = WritePassiveRegister()

        quantity, value = struct.unpack('>BH', resp_pdu[1:4])

        write_passive_register._address = quantity
        write_passive_register.data = value

        return write_passive_register


    def execute(self, slave_id, route_map):
        """ Execute the Modbus function registered for a route.

        :param slave_id: Slave id.
        :param eindpoint: Instance of modbus.route.Map.
        """
        endpoint = route_map.match(slave_id, self.function_code, self._address)
        try:
            endpoint(slave_id=slave_id, 
                     address=self._address, 
                     value=self._value,
                     function_code=self.function_code)
        # route_map.match() returns None if no match is found. Calling None
        # results in TypeError.
        except TypeError:
            raise IllegalDataAddressError()


function_code_to_function_map[WRITE_PASSIVE_REGISTER] = WritePassiveRegister
