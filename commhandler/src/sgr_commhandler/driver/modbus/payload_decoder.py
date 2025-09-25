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
        super().__init__(*args, **kwargs)

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
        if modbus_type.int8:
            return self.decode_8bit_int()
        elif modbus_type.int8_u:
            return self.decode_8bit_uint()
        elif modbus_type.int16:
            return self.decode_16bit_int()
        elif modbus_type.int16_u:
            return self.decode_16bit_uint()
        elif modbus_type.int32:
            return self.decode_32bit_int()
        elif modbus_type.int32_u:
            return self.decode_32bit_uint()
        elif modbus_type.int64:
            return self.decode_64bit_int()
        elif modbus_type.int64_u:
            return self.decode_64bit_uint()
        elif modbus_type.float32:
            return self.decode_32bit_float()
        elif modbus_type.float64:
            return self.decode_64bit_float()
        elif modbus_type.boolean:
            return bool(self.decode_8bit_uint())
        elif modbus_type.string:
            return self.decode_string(byte_count)
        else:
            raise ValueError("No supported modbus data type")


class PayloadBuilder(BinaryPayloadBuilder):
    """
    Implements a Modbus payload encoder.
    """

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

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
        if modbus_type.int8:
            self.add_8bit_int(int(value))
        elif modbus_type.int8_u:
            self.add_8bit_uint(int(value))
        elif modbus_type.int16:
            self.add_16bit_int(int(value))
        elif modbus_type.int16_u:
            self.add_16bit_uint(int(value))
        elif modbus_type.int32:
            self.add_32bit_int(int(value))
        elif modbus_type.int32_u:
            self.add_32bit_uint(int(value))
        elif modbus_type.int64:
            self.add_64bit_int(int(value))
        elif modbus_type.int64_u:
            self.add_64bit_uint(int(value))
        elif modbus_type.float32:
            self.add_32bit_float(float(value))
        elif modbus_type.float64:
            self.add_64bit_float(float(value))
        elif modbus_type.boolean:
            self.add_8bit_uint(bool(value))
        elif modbus_type.string:
            self.add_string(str(value))
        else:
            logger.error(f'Unsupported modbus type "{modbus_type}"')
        return self
