"""
Provides the Modbus client implementation.
"""

import logging
import threading
from abc import ABC
from typing import Any, Literal

from pymodbus import FramerType
from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from sgr_specification.v0.product.modbus_types import BitOrder, ModbusDataType

from sgr_commhandler.driver.modbus.modbus_helper import (
    AnyModbusClient,
    decode_registers,
    encode_registers
)


logger = logging.getLogger(__name__)


class SGrModbusClient(ABC):
    """
    Defines an abstract base class for Modbus clients.
    """

    def __init__(self, bit_order: BitOrder, addr_offset: int, client: AnyModbusClient):
        self._lock = threading.Lock()
        self._client: AnyModbusClient = client
        self._byte_order: Literal['big', 'little'] = (
            'little'
            if bit_order
            in {BitOrder.CHANGE_BYTE_ORDER, BitOrder.CHANGE_BIT_ORDER}
            else 'big'
        )
        self._word_order: Literal['big', 'little'] = (
            'little'
            if bit_order
            in {BitOrder.CHANGE_WORD_ORDER, BitOrder.CHANGE_DWORD_ORDER}
            else 'big'
        )
        self._addr_offset: int = addr_offset

    async def connect(self): ...

    async def disconnect(self): ...

    def is_connected(self) -> bool: ...

    async def write_holding_registers(
        self, slave_id: int, address: int, data_type: ModbusDataType, value: Any
    ):
        """
        Encodes value to be written to holding register address.

        Parameters
        ----------
        slave_id : int
            The slave ID of the device
        address : int
            The address to read from and decode
        data_type : ModbusDataType
            The modbus type to encode
        value : Any
            The value to be written
        """
        registers = encode_registers(self._client, value, data_type, word_order=self._word_order, byte_order=self._byte_order)
        with self._lock:
            response = await self._client.write_registers(
                address+self._addr_offset, registers, device_id=slave_id, no_response_expected=False
            )
            if response is not None and response.isError():
                logger.warning(f'Modbus write exception {response.function_code}')
            elif response is None:
                logger.warning('Modbus write did not get response')

    async def write_coils(
        self, slave_id: int, address: int, data_type: ModbusDataType, value: Any
    ):
        """
        Encodes value to be written to coil address.

        Parameters
        ----------
        slave_id : int
            The slave ID of the device
        address : int
            The address to read from and decode
        data_type : ModbusDataType
            The modbus type to encode
        value : Any
            The value to be written
        """
        # TODO implement conversion
        bits: list[bool] = []
        with self._lock:
            response = await self._client.write_coils(
                address+self._addr_offset, bits, device_id=slave_id, no_response_expected=True
            )
            if response is not None and response.isError():
                logger.warning(f'Modbus write exception {response.function_code}')
            elif response is None:
                logger.warning('Modbus write did not get response')

    async def read_input_registers(
        self, slave_id: int, address: int, size: int, data_type: ModbusDataType
    ) -> Any:
        """
        Reads input registers and decodes the value.

        Parameters
        ----------
        slave_id : int
            The slave ID of the device
        address : int
            The address to read from and decode
        size : int
            The number of registers to read
        data_type : ModbusDataType
            The modbus type to decode

        Returns
        -------
        Any
            Decoded value
        """
        with self._lock:
            response = await self._client.read_input_registers(
                address+self._addr_offset, count=size, device_id=slave_id
            )
        if response is not None and not response.isError():
            return decode_registers(self._client, response.registers, data_type, word_order=self._word_order, byte_order=self._byte_order)
        elif response is not None and response.isError():
            logger.warning(f'Modbus read exception {response.function_code}')
        elif response is None:
            logger.warning('Modbus read did not get response')

    async def read_holding_registers(
        self, slave_id: int, address: int, size: int, data_type: ModbusDataType
    ) -> Any:
        """
        Reads holding registers and decodes the value.

        Parameters
        ----------
        slave_id : int
            The slave ID of the device
        address : int
            The address to read from and decode
        size : int
            The number of registers to read
        data_type : ModbusDataType
            The modbus type to decode

        Returns
        -------
        Any
            Decoded value
        """
        with self._lock:
            response = await self._client.read_holding_registers(
                address+self._addr_offset, count=size, device_id=slave_id
            )
        if response is not None and not response.isError():
            return decode_registers(self._client, response.registers, data_type, word_order=self._word_order, byte_order=self._byte_order)
        elif response is not None and response.isError():
            logger.warning(f'Modbus read exception {response.function_code}')
        elif response is None:
            logger.warning('Modbus read did not get response')

    async def read_coils(
        self, slave_id: int, address: int, size: int, data_type: ModbusDataType
    ) -> Any:
        """
        Reads coils and decodes the value.

        Parameters
        ----------
        slave_id : int
            The slave ID of the device
        address : int
            The address to read from and decode
        size : int
            The number of coils to read
        data_type : ModbusDataType
            The modbus type to decode

        Returns
        -------
        Any
            Decoded value
        """
        with self._lock:
            response = await self._client.read_coils(
                address+self._addr_offset, count=size, device_id=slave_id
            )
        if response is not None and not response.isError():
            # TODO implement conversion
            return response.bits
        elif response is not None and response.isError():
            logger.warning(f'Modbus read exception {response.function_code}')
        elif response is None:
            logger.warning('Modbus read did not get response')

    async def read_discrete_inputs(
        self, slave_id: int, address: int, size: int, data_type: ModbusDataType
    ) -> Any:
        """
        Reads discrete inputs and decodes the value.

        Parameters
        ----------
        slave_id : int
            The slave ID of the device
        address : int
            The address to read from and decode
        size : int
            The number of inputs to read
        data_type : ModbusDataType
            The modbus type to decode

        Returns
        -------
        Any
            Decoded value
        """
        with self._lock:
            response = await self._client.read_discrete_inputs(
                address+self._addr_offset, count=size, device_id=slave_id
            )
        if response is not None and not response.isError():
            # TODO implement conversion
            return response.bits
        elif response is not None and response.isError():
            logger.warning(f'Modbus read exception {response.function_code}')
        elif response is None:
            logger.warning('Modbus read did not get response')


class SGrModbusTCPClient(SGrModbusClient):
    """
    Implements a Modbus TCP client.
    """

    def __init__(self, ip: str, port: int, bit_order: BitOrder = BitOrder.BIG_ENDIAN, addr_offset: int = 0):
        super(SGrModbusTCPClient, self).__init__(
            bit_order,
            addr_offset,
            AsyncModbusTcpClient(
                host=ip,
                port=port,
                timeout=1.0,
                retries=0,
                reconnect_delay=1.0,
                reconnect_delay_max=30.0
            )
        )
        """
        Creates client.

        Parameters
        ----------
        ip : str
            The host to connect to (default 127.0.0.1)
        port : int
            The modbus port to connect to (default 502)
        bit_order : BitOrder
            The data byte or word order
        addr_offset : int
            The address offset
        """
        self._ip = ip
        self._port = port

    async def connect(self):
        with self._lock:
            await self._client.connect()
            logger.debug('Connected to ModbusTCP on ip: ' + self._ip)

    async def disconnect(self):
        with self._lock:
            self._client.close()
            logger.debug('Disconnected from ModbusTCP on ip: ' + self._ip)

    def is_connected(self) -> bool:
        return self._client.connected


class SGrModbusRTUClient(SGrModbusClient):
    def __init__(
        self, serial_port: str, parity: str, baudrate: int, bit_order: BitOrder = BitOrder.BIG_ENDIAN, addr_offset: int = 0
    ):
        super(SGrModbusRTUClient, self).__init__(
            bit_order,
            addr_offset,
            AsyncModbusSerialClient(
                port=serial_port,
                framer=FramerType.RTU,
                parity=parity,
                baudrate=baudrate
            )
        )
        """
        Creates client.

        Parameters
        ----------
        serial_port : str
            The serial port to connect to (e.g. COM1)
        parity : str
            The serial parity (e.g. EVEN)
        baudrate : int
            The serial baudrate (e.g. 19200)
        bit_order : BitOrder
            The data byte or word order
        addr_offset : int
            The address offset
        """
        self._serial_port = serial_port

    async def connect(self):
        with self._lock:
            await self._client.connect()
            logger.debug(
                'Connected to ModbusRTU on serial port: ' + self._serial_port
            )

    async def disconnect(self):
        with self._lock:
            self._client.close()
            logger.debug(
                'Disconnected from ModbusRTU on serial port: '
                + self._serial_port
            )

    def is_connected(self) -> bool:
        return self._client.connected
