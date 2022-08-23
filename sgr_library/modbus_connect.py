from sgr_library.payload_decoder import PayloadDecoder, PayloadBuilder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient


# In this case establishes a connection with the localhost server that is running the simulation.
class ModbusConnect:

    def __init__(self, ip, port) -> None:
        #EXAMPLE: client = ModbusTcpClient('127.0.0.1', 5002)
        self.client = ModbusTcpClient(ip, port)
        self.client.connect()

    def value_decoder(self, addr, size, reg_type):
        reg = self.client.read_holding_registers(addr, count=size)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        
        if not reg.isError():
            return decoder.decode(reg_type, 0)

    def value_encoder(self, addr, value, reg_type):
        builder = PayloadBuilder(byteorder=Endian.Little, wordorder=Endian.Little)
        builder.encode(value, reg_type, rounding="floor")
        self.client.write_registers(address=addr, values=builder.to_registers(), unit=0)
