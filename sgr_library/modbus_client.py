from sgr_library.payload_decoder import PayloadDecoder, PayloadBuilder
from pymodbus.constants import Endian
from pymodbus.client import AsyncModbusTcpClient
from typing import Optional, Tuple, Dict, Any, Iterable


# In this case establishes a connection with the localhost server that is running the simulation.
# TODO make this inherit from the ModbusTcpClient
# TODO maybe make everything in one module... Modulating this is redundant in my taste.
class SGrModbusClient:

    def __init__(self, ip: str, port: int):
        """
        Creates client
        :param ip: The host to connect to (default 127.0.0.1)
        :param port: The modbus port to connect to (default 502)
        """
        #EXAMPLE: client = ModbusTcpClient('127.0.0.1', 5002)
        self.client = AsyncModbusTcpClient(
        host=ip,
        port=port,
        timeout=1,
        retries=0,
        reconnect_delay=5000,
        close_comm_on_error=False,)
        #self.client.connect() #TODO a wrapper that opens and closes connection when function is excecuted?

    async def value_decoder(self, addr: int, size: int, data_type: str, register_type: str, slave_id: int, order: Endian) -> Optional[float]:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        if register_type == "HoldRegister":
            reg = await self.client.read_holding_registers(addr, size, slave=slave_id) #TODO add slave id?
        else:
            reg = await self.client.read_input_registers(addr, count=size, unit=slave_id)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=order, wordorder=order)
        #print(decoder.decode('float32', 0))
        if not reg.isError():
            #await print(decoder.decode(data_type, 0))
            return decoder.decode(data_type, 0)
        
    async def mult_value_decoder(self, addr: int, size: int, data_type: str, register_type: str, slave_id: int, order: Endian) -> Optional[float]:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        if register_type == "HoldRegister":
            reg = await self.client.read_holding_registers(addr, size, slave=slave_id) #TODO add slave id?
        else:
            reg = await self.client.read_input_registers(addr, count=size, unit=slave_id)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=order, wordorder=order)
        #print(decoder.decode('float32', 0))
        if not reg.isError():
            #await print(decoder.decode(data_type, 0))
            indexes = [size//3*0, size//3*1, size//3*2]
            l1 = decoder.decode(data_type, indexes[0])
            l2 = decoder.decode(data_type, indexes[1])
            l3 = decoder.decode(data_type, indexes[2])
            return l1, l2, l3


    async def value_encoder(self, addr: int, value: float, data_type: str, slave_id: int, order: Endian):
        """
        Encodes value to be set on the register address
        :param addr: The address to read from and decode
        :param value: The value to be written on the register
        :param data_type: The modbus type to decode
        """
        builder = PayloadBuilder(byteorder=order, wordorder=order)
        builder.encode(value, data_type, rounding="floor")
        await self.client.write_registers(address=addr, values=builder.to_registers(), unit=slave_id)

