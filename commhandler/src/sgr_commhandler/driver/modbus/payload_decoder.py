"""
Provides a payload encoder and decoder to convert between external and Modbus data types.
This implementation is only supported up to pymodbus 3.8.
"""

import logging
from typing import Any

from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from sgr_specification.v0.product.modbus_types import ModbusDataType


logger = logging.getLogger(__name__)


class PayloadDecoder(BinaryPayloadDecoder):
    """
    Implements a Modbus payload decoder.
    """

    def __init__(self, *args, **kwargs):
        super(PayloadDecoder, self).__init__(*args, **kwargs)

    def decode(self, modbus_type: ModbusDataType, byte_count: int):
        """
        Decodes a data value.

        Parameters
        ----------
        modbus_type : ModbusDataType
            the Modbus data type to decode
        byte_count : int
            the number of bytes

        Returns
        -------
        Any
            the decoded value
        """

        # TODO enum, date_time
        if modbus_type.int8 is not None:
            return self.decode_8bit_int()
        elif modbus_type.int8_u is not None:
            return self.decode_8bit_uint()
        elif modbus_type.int16 is not None:
            return self.decode_16bit_int()
        elif modbus_type.int16_u is not None:
            return self.decode_16bit_uint()
        elif modbus_type.int32 is not None:
            return self.decode_32bit_int()
        elif modbus_type.int32_u is not None:
            return self.decode_32bit_uint()
        elif modbus_type.int64 is not None:
            return self.decode_64bit_int()
        elif modbus_type.int64_u is not None:
            return self.decode_64bit_uint()
        elif modbus_type.float32 is not None:
            return self.decode_32bit_float()
        elif modbus_type.float64 is not None:
            return self.decode_64bit_float()
        elif modbus_type.boolean is not None:
            return bool(self.decode_8bit_uint())
        elif modbus_type.string is not None:
            str_bytes = self.decode_string(byte_count)
            logger.debug(f'bytes={byte_count}, res={str_bytes.__repr__()}')
            return str_bytes.decode()
        else:
            raise ValueError("No supported modbus data type")


class PayloadBuilder(BinaryPayloadBuilder):
    """
    Implements a Modbus payload encoder.
    """

    def __init__(self, *args, **kwarg):
        super(PayloadBuilder, self).__init__(*args, **kwarg)

    def sgr_encode(
        self, value: Any, modbus_type: ModbusDataType
    ) -> "PayloadBuilder":
        """
        Encodes data type value.

        Parameters
        ----------
        value : Any
            the value to encode
        modbus_type : ModbusDataType
            The Modbus data type to encode

        Returns
        -------
        PayloadBuilder
            the same instance
        """
        # TODO enum, date_time
        if modbus_type.int8 is not None:
            self.add_8bit_int(int(value))
        elif modbus_type.int8_u is not None:
            self.add_8bit_uint(int(value))
        elif modbus_type.int16 is not None:
            self.add_16bit_int(int(value))
        elif modbus_type.int16_u is not None:
            self.add_16bit_uint(int(value))
        elif modbus_type.int32 is not None:
            self.add_32bit_int(int(value))
        elif modbus_type.int32_u is not None:
            self.add_32bit_uint(int(value))
        elif modbus_type.int64 is not None:
            self.add_64bit_int(int(value))
        elif modbus_type.int64_u is not None:
            self.add_64bit_uint(int(value))
        elif modbus_type.float32 is not None:
            self.add_32bit_float(float(value))
        elif modbus_type.float64 is not None:
            self.add_64bit_float(float(value))
        elif modbus_type.boolean is not None:
            self.add_8bit_uint(bool(value))
        elif modbus_type.string is not None:
            self.add_string(str(value))
        else:
            logger.error(f'Unsupported Modbus type "{modbus_type}"')
        return self
