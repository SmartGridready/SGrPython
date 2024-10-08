from abc import ABC, abstractmethod
import asyncio
import logging
from typing import Optional
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
from pymodbus.constants import Endian
from sgr_commhandler.driver.modbus.payload_decoder import (
    PayloadBuilder,
    PayloadDecoder,
    RoundingScheme,
)

logger = logging.getLogger(__name__)


class SGrModbusClient(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def is_connected(self):
        pass

    async def value_encoder(
        self,
        addr: int,
        value: float,
        data_type: str,
        slave_id: int,
        order: Endian,
    ):
        """
        Encodes value to be set on the register address
        :param addr: The address to read from and decode
        :param value: The value to be written on the register
        :param data_type: The modbus type to decode
        """
        async with self._semaphore:
            builder = PayloadBuilder(byteorder=order, wordorder=order)
            builder.encode(value, data_type, rounding=RoundingScheme.floor)
            await self.client.write_registers(
                address=addr, values=builder.to_registers(), unit=slave_id
            )

    async def value_decoder(
        self,
        addr: int,
        size: int,
        data_type: str,
        register_type: str,
        slave_id: int,
        order: Endian,
    ) -> float:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        async with self._semaphore:
            if (
                register_type == "HoldRegister"
            ):  # Todo im Modbus_client ist "HoldingRegister" angeben, ist das falsch?
                reg = await self.client.read_holding_registers(
                    addr, count=size, slave=slave_id
                )
                # logger.debug(reg.registers)
            else:
                reg = await self.client.read_input_registers(
                    addr, count=size, slave=slave_id
                )
            decoder = PayloadDecoder.fromRegisters(
                reg.registers, byteorder=order, wordorder=order
            )

            if not reg.isError():
                return decoder.decode(data_type, 0)

    # TODO Under construction
    async def mult_value_decoder(
        self,
        addr: int,
        size: int,
        data_type: str,
        register_type: str,
        slave_id: int,
        order: Endian,
    ) -> Optional[float]:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        if register_type == "HoldRegister":
            reg = self._client.read_holding_registers(
                addr, size, slave=slave_id
            )  # TODO add slave id?
        else:
            reg = self._client.read_input_registers(
                addr, count=size, slave=slave_id
            )
        decoder = PayloadDecoder.fromRegisters(
            reg.registers, byteorder=order, wordorder=order
        )
        # logger.debug(decoder.decode('float32', 0))
        if not reg.isError():
            # logger.debug(decoder.decode(data_type, 0))
            indexes = [size // 3 * 0, size // 3 * 1, size // 3 * 2]
            l1 = decoder.decode(data_type, indexes[0])
            l2 = decoder.decode(data_type, indexes[1])
            l3 = decoder.decode(data_type, indexes[2])
            return l1, l2, l3


class SGrModbusTCPClient(SGrModbusClient):
    def __init__(self, ip: str, port: int):
        """
        Creates client
        :param ip: The host to connect to (default 127.0.0.1)
        :param port: The modbus port to connect to (default 502)
        """
        self._ip = ip
        # EXAMPLE: client = ModbusTcpClient('127.0.0.1', 5002)
        self._client = AsyncModbusTcpClient(
            host=ip,
            port=port,
            timeout=1,
            retries=0,
            reconnect_delay=5000,
            reconnect_delay_max=30000,
        )

    async def connect(self):
        await self._client.connect()
        logger.debug("Connected to ModbusTCP on ip: " + self._ip)

    async def disconnect(self):
        await self._client.close()
        logger.debug("Disconnected from ModbusTCP on ip: " + self._ip)

    async def is_connected(self):
        await self._client.connected


class SGrModbusRTUClient(SGrModbusClient):
    def __init__(self, serial_port: str, parity: str, baudrate: int, client=None):
        """
        Creates client
        :param serial_port: The serial port to connect to (e.g. COM1)
        :param parity: The serial parity (e.g. EVEN)
        :param baudrate: The serial baudrate (e.g. 19200)
        """
        self._serial_port = serial_port
        self._semaphore = asyncio.Semaphore(1)
        if client is not None:
            self._client = client
        else:
            self._client = AsyncModbusSerialClient(
                method="rtu",
                port=serial_port,
                parity=parity,
                baudrate=baudrate,
            )  # changed source: https://stackoverflow.com/questions/58773476/why-do-i-get-pymodbus-modbusioexception-on-20-of-attempts

    async def connect(self):
        await self._client.connect()
        logger.debug("Connected to ModbusRTU on serial port: " + self._serial_port)

    async def disconnect(self):
        await self._client.close()
        logger.debug("Disconnected from ModbusRTU on serial port: " + self._serial_port)

    async def is_connected(self):
        await self._client.connected
