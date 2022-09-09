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
        """
        :param modbus_type: 'int8', 'int8_u', 'int16', 'int16_u', 'int32', 'int32_u', 'int64', 'int64_u', 'float16', 'float32', 'float64', 'string'
        """
        # TODO boolean, enum, date_time
        if modbus_type == 'int8':
            return self.decode_8bit_int()
        elif modbus_type == 'int8_u':
            return self.decode_8bit_uint()
        elif modbus_type == 'int16':
            return self.decode_16bit_int()
        elif modbus_type == 'int16_u':
            return self.decode_16bit_uint()
        elif modbus_type == 'int32':
            return self.decode_32bit_int()
        elif modbus_type == 'int32_u':
            return self.decode_32bit_uint()
        elif modbus_type == 'int64':
            return self.decode_64bit_int()
        elif modbus_type == 'int64_u':
            return self.decode_64bit_uint()
        elif modbus_type == 'float16':
            return self.decode_16bit_float()
        elif modbus_type == 'float32':
            return self.decode_32bit_float()
        elif modbus_type == 'float64':
            return self.decode_32bit_float()
        elif modbus_type == 'string':
            return self.decode_string(byte_count)
        else:
            pass


class PayloadBuilder(BinaryPayloadBuilder):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

    def encode(self, value: float, modbus_type: str, rounding: RoundingScheme):
        """
        :param modbus_type: 'int8', 'int8_u', 'int16', 'int16_u', 'int32', 'int32_u', 'int64', 'int64_u', 'float16', 'float32', 'float64', 'string'
        """
        # TODO boolean, int8, int8_u, enum, date_time
        if modbus_type == 'int8':
            self.add_8bit_int(round_to_int(value, rounding))
        elif modbus_type == 'int8_u':
            self.add_8bit_uint(round_to_int(value, rounding))
        elif modbus_type == 'int16':
            self.add_16bit_int(round_to_int(value, rounding))
        elif modbus_type == 'int16_u':
            self.add_16bit_uint(round_to_int(value, rounding))
        elif modbus_type == 'int32':
            self.add_32bit_int(round_to_int(value, rounding))
        elif modbus_type == 'int32_u':
            self.add_32bit_uint(round_to_int(value, rounding))
        elif modbus_type == 'int64':
            self.add_64bit_int(round_to_int(value, rounding))
        elif modbus_type == 'int64_u':
            self.add_64bit_uint(round_to_int(value, rounding))
        elif modbus_type == 'float16':
            self.add_16bit_float(round_to_int(value, rounding))
        elif modbus_type == 'float32':
            self.add_32bit_float(round_to_int(value, rounding))
        elif modbus_type == 'float64':
            self.add_64bit_float(round_to_int(value, rounding))
        elif modbus_type == 'string':
            self.add_string(round_to_int(value, rounding))
        else:
            print('Unknown modbus type "%s"', modbus_type)







