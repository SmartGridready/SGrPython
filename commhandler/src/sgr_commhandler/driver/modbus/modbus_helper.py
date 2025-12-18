from typing import Any, Literal, TypeAlias
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
from pymodbus.client.mixin import ModbusClientMixin
from sgr_specification.v0.product.modbus_types import ModbusDataType

AnyModbusClient: TypeAlias = AsyncModbusSerialClient | AsyncModbusTcpClient


def decode_registers(client: AnyModbusClient,
                     registers: list[int], data_type: ModbusDataType,
                     word_order: Literal['big', 'little'] = 'big', byte_order: Literal['big', 'little'] = 'big') -> Any:
    if byte_order == 'little':
        for i in range(0, len(registers)):
            registers[i] = change_byte_order(registers[i])
    return client.convert_from_registers(registers, data_type=get_data_type(data_type), word_order=word_order)


def encode_registers(client: AnyModbusClient,
                     value: Any, data_type: ModbusDataType,
                     word_order: Literal['big', 'little'] = 'big', byte_order: Literal['big', 'little'] = 'big') -> list[int]:
    registers = client.convert_to_registers(value, data_type=get_data_type(data_type), word_order=word_order)
    if byte_order == 'little':
        for i in range(0, len(registers)):
            registers[i] = change_byte_order(registers[i])
    return registers


def change_byte_order(word: int) -> int:
    # pymodbus delivers register values as uint16 (0..65535)
    if word < 0 or word > 65535:
        raise Exception(f'value {word} out of bounds')
    lb = word & 0xFF
    hb = word >> 8 & 0xFF
    return lb << 8 | hb


def registers_as_hex(registers: list[int]) -> str:
    registers_str = map(lambda rr: f'{rr:04x}', registers)
    return str.join(' ', registers_str)


def get_data_type(modbus_type: ModbusDataType) -> ModbusClientMixin.DATATYPE:
    if modbus_type.int8 is not None:
        # TODO test if this works
        return ModbusClientMixin.DATATYPE.INT16
    elif modbus_type.int8_u is not None:
        # TODO test if this works
        return ModbusClientMixin.DATATYPE.UINT16
    elif modbus_type.int16 is not None:
        return ModbusClientMixin.DATATYPE.INT16
    elif modbus_type.int16_u is not None:
        return ModbusClientMixin.DATATYPE.UINT16
    elif modbus_type.int32 is not None:
        return ModbusClientMixin.DATATYPE.INT32
    elif modbus_type.int32_u is not None:
        return ModbusClientMixin.DATATYPE.UINT32
    elif modbus_type.int64 is not None:
        return ModbusClientMixin.DATATYPE.INT64
    elif modbus_type.int64_u is not None:
        return ModbusClientMixin.DATATYPE.UINT64
    elif modbus_type.float32 is not None:
        return ModbusClientMixin.DATATYPE.FLOAT32
    elif modbus_type.float64 is not None:
        return ModbusClientMixin.DATATYPE.FLOAT64
    elif modbus_type.boolean is not None:
        # TODO test if this works
        return ModbusClientMixin.DATATYPE.UINT16
    elif modbus_type.string is not None:
        return ModbusClientMixin.DATATYPE.STRING
    else:
        raise ValueError("No supported modbus data type")
