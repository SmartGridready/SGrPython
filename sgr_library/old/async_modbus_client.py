from sgr_library.payload_decoder import PayloadDecoder, PayloadBuilder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient

from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient

# In this case establishes a connection with the localhost server that is running the simulation.
# TODO make this inherit from the ModbusTcpClient
class SGrModbusClient:

    def __init__(self, ip: str, port: str):
        """
        Creates client
        :param ip: The host to connect to (default 127.0.0.1)
        :param port: The modbus port to connect to (default 502)
        """
        #EXAMPLE: client = ModbusTcpClient('127.0.0.1', 5002)
        self.client = AsyncModbusTCPClient(host=ip, port=port)
        #self.client = ModbusTcpClient(ip, port)
        self.client.connect() #TODO a wrapper that opens and closes connection when function is excecuted?

    def value_decoder(
        self, addr: int, size: int, data_type: str, register_type: str, 
        slave_id: int, order: Endian) -> float:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        if register_type == "HoldingRegister":
            reg = self.client.read_holding_registers(addr, count=size, unit=slave_id) #TODO add slave id?
        else:
            reg = self.client.read_input_registers(addr, count=size, unit=slave_id)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=order, wordorder=order)
        if not reg.isError():
            return decoder.decode(data_type, 0)

    def value_encoder(self, addr: int, value: float, data_type: str, slave_id: int, order: Endian):
        """
        Encodes value to be set on the register address
        :param addr: The address to read from and decode
        :param value: The value to be written on the register
        :param data_type: The modbus type to decode
        """
        builder = PayloadBuilder(byteorder=order, wordorder=order)
        builder.encode(value, data_type, rounding="floor")
        self.client.write_registers(address=addr, values=builder.to_registers(), unit=slave_id)
