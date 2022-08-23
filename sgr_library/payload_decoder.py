from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from numpy import ceil, floor, rint
from enum import Enum


class RoundingScheme(Enum):
    floor = 'floor'
    ceil = 'ceil'
    near = 'Near'

def round_to_int(value: float, scheme: RoundingScheme) -> int:
    if scheme == RoundingScheme.floor:
        return int(floor(value))
    elif scheme == RoundingScheme.ceil:
        return int(ceil(value))
    elif scheme == RoundingScheme.near:
        return int(rint(value))
    else:
        print(
            'tried rounding with a invalid scheme (%s) using floor instead', scheme
        )
        return int(floor(value))


class PayloadDecoder(BinaryPayloadDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, modbus_type: str, byte_count: int):
        if modbus_type == 'INT16':
            return self.decode_16bit_int()
        elif modbus_type == 'INT16u':
            return self.decode_16bit_uint()
        elif modbus_type == 'INT32':
            return self.decode_32bit_int()
        elif modbus_type == 'INT32u':
            return self.decode_32bit_uint()
        elif modbus_type == 'INT64':
            return self.decode_64bit_int()
        elif modbus_type == 'INT64u':
            return self.decode_64bit_uint()
        elif modbus_type == 'FLOAT32':
            return self.decode_32bit_float()
        elif modbus_type == 'FLOAT64':
            return self.decode_32bit_float()
        elif modbus_type == 'STRING':
            return self.decode_string(byte_count)
        else:
            pass


class PayloadBuilder(BinaryPayloadBuilder):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

    def encode(self, value: float, modbus_type: str, rounding: RoundingScheme):
        if modbus_type == 'INT16':
            self.add_16bit_int(round_to_int(value, rounding))
        elif modbus_type == 'INT16u':
            self.add_16bit_uint(round_to_int(value, rounding))
        elif modbus_type == 'INT32':
            self.add_32bit_int(round_to_int(value, rounding))
        elif modbus_type == 'INT32u':
            self.add_32bit_uint(round_to_int(value, rounding))
        elif modbus_type == 'INT64':
            self.add_64bit_int(round_to_int(value, rounding))
        elif modbus_type == 'INT64u':
            self.add_64bit_uint(round_to_int(value, rounding))
        else:
            print('Unknown modbus type "%s"', modbus_type)
