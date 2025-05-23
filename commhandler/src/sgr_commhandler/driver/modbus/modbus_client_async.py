import logging
import threading
from abc import ABC
from typing import Any, Optional

from pymodbus import FramerType
from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus.client.base import ModbusBaseClient
from pymodbus.constants import Endian
from sgr_specification.v0.product.modbus_types import BitOrder, ModbusDataType

from sgr_commhandler.driver.modbus.payload_decoder import (
    PayloadBuilder,
    PayloadDecoder,
)

logger = logging.getLogger(__name__)


class SGrModbusClient(ABC):
    """
    Defines an abstract base class for Modbus clients.
    """

    def __init__(self, endianness: BitOrder, addr_offset: int):
        self._lock = threading.Lock()
        self._client: Optional[ModbusBaseClient] = None
        self._byte_order: Endian = (
            Endian.BIG
            if endianness is None or endianness == BitOrder.BIG_ENDIAN
            else Endian.LITTLE
        )
        self._word_order: Endian = (
            Endian.LITTLE
            if endianness
            in {BitOrder.CHANGE_WORD_ORDER, BitOrder.CHANGE_DWORD_ORDER}
            else Endian.BIG
        )
        self._addr_offset = addr_offset

    async def connect(self): ...

    async def disconnect(self): ...

    def is_connected(self) -> bool: ...

    async def write_holding_registers(
        self, slave_id: int, address: int, data_type: ModbusDataType, value: Any
    ) -> None:
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
        if self._client is None:
            raise Exception('Client not initialized')
        builder = PayloadBuilder(
            byteorder=self._byte_order, wordorder=self._word_order
        )
        builder.sgr_encode(value, data_type)
        with self._lock:
            await self._client.write_registers(
                address+self._addr_offset, builder.to_registers(), slave=slave_id
            )

    async def write_coils(
        self, slave_id: int, address: int, data_type: ModbusDataType, value: Any
    ) -> None:
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
        if self._client is None:
            raise Exception('Client not initialized')
        builder = PayloadBuilder(
            byteorder=self._byte_order, wordorder=self._word_order
        )
        builder.sgr_encode(value, data_type)
        with self._lock:
            await self._client.write_coils(
                address+self._addr_offset, builder.to_coils(), slave=slave_id
            )

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
        if self._client is None:
            raise Exception('Client not initialized')
        with self._lock:
            response = await self._client.read_input_registers(
                address+self._addr_offset, count=size, slave=slave_id
            )
        if response and not response.isError():
            decoder = PayloadDecoder.fromRegisters(
                response.registers,
                byteorder=self._byte_order,
                wordorder=self._word_order,
            )
            return decoder.decode(data_type, 0)

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
        if self._client is None:
            raise Exception('Client not initialized')
        with self._lock:
            response = await self._client.read_holding_registers(
                address+self._addr_offset, count=size, slave=slave_id
            )
        if response and not response.isError():
            decoder = PayloadDecoder.fromRegisters(
                response.registers,
                byteorder=self._byte_order,
                wordorder=self._word_order,
            )
            return decoder.decode(data_type, 0)

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
        if self._client is None:
            raise Exception('Client not initialized')
        with self._lock:
            response = await self._client.read_coils(
                address+self._addr_offset, count=size, slave=slave_id
            )
        if response and not response.isError():
            decoder = PayloadDecoder.fromCoils(
                response.bits,
                byteorder=self._byte_order,
                _wordorder=self._word_order,
            )
            return decoder.decode(data_type, 0)

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
        if self._client is None:
            raise Exception('Client not initialized')
        with self._lock:
            response = await self._client.read_discrete_inputs(
                address+self._addr_offset, count=size, slave=slave_id
            )
        if response and not response.isError():
            decoder = PayloadDecoder.fromCoils(
                response.bits,
                byteorder=self._byte_order,
                _wordorder=self._word_order,
            )
            return decoder.decode(data_type, 0)

    # TODO Implement block transfers and remove this method
    async def _mult_value_decoder(
        self,
        addr: int,
        size: int,
        data_type: ModbusDataType,
        register_type: str,
        slave_id: int,
    ) -> Optional[tuple[float,float,float]]:
        """
        Reads register and decodes the value.

        Parameters
        ----------
        addr : int
            The address to read from and decode
        size : int
            The number of registers to read
        data_type : ModbusDataType
            The modbus type to decode
        register_type : str
            The register type
        slave_id : int
            The slave ID of the device 

        Returns
        -------
        Optional[tuple[float,float,float]]
            Decoded float tuple
        """
        if self._client is None:
            raise Exception('Client not initialized')
        if register_type == 'HoldRegister':
            reg = self._client.read_holding_registers(
                addr, count=size, slave=slave_id
            )
        else:
            reg = self._client.read_input_registers(
                addr, count=size, slave=slave_id
            )
        reg = await reg
        decoder = PayloadDecoder.fromRegisters(
            reg.registers,
            byteorder=self._byte_order,
            wordorder=self._word_order,
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
    """
    Implements a Modbus TCP client.
    """

    def __init__(self, ip: str, port: int, endianness: BitOrder = BitOrder.BIG_ENDIAN, addr_offset: int = 0):
        super().__init__(endianness, addr_offset)
        """
        Creates client.

        Parameters
        ----------
        ip : str
            The host to connect to (default 127.0.0.1)
        port : int
            The modbus port to connect to (default 502)
        endianness : BitOrder
            The data endianness
        addr_offset : int
            The address offset
        """
        self._ip = ip
        self._port = port
        self._client = AsyncModbusTcpClient(
            host=ip,
            port=port,
            timeout=1,
            retries=0,
            reconnect_delay=5000,
            reconnect_delay_max=30000,
        )

    async def connect(self):
        if self._client is None:
            raise Exception('Client not initialized')

        with self._lock:
            await self._client.connect()
            logger.debug('Connected to ModbusTCP on ip: ' + self._ip)

    async def disconnect(self):
        if self._client is None:
            return
        with self._lock:
            self._client.close()
            logger.debug('Disconnected from ModbusTCP on ip: ' + self._ip)

    def is_connected(self) -> bool:
        return self._client is not None and self._client.connected


class SGrModbusRTUClient(SGrModbusClient):
    def __init__(
        self, serial_port: str, parity: str, baudrate: int, endianness: BitOrder = BitOrder.BIG_ENDIAN, addr_offset: int = 0
    ):
        super().__init__(endianness, addr_offset)
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
        endianness : BitOrder
            The data endianness
        addr_offset : int
            The address offset
        """
        self._serial_port = serial_port
        self._client = AsyncModbusSerialClient(
            port=serial_port,
            framer=FramerType.RTU,
            parity=parity,
            baudrate=baudrate,
        )  # changed source: https://stackoverflow.com/questions/58773476/why-do-i-get-pymodbus-modbusioexception-on-20-of-attempts

    async def connect(self):
        if self._client is None:
            raise Exception('Client not initialized')
        with self._lock:
            await self._client.connect()
            logger.debug(
                'Connected to ModbusRTU on serial port: ' + self._serial_port
            )

    async def disconnect(self):
        if self._client is None:
            raise Exception('Client not initialized')
        with self._lock:
            self._client.close()
            logger.debug(
                'Disconnected from ModbusRTU on serial port: '
                + self._serial_port
            )

    def is_connected(self) -> bool:
        return self._client is not None and self._client.connected
