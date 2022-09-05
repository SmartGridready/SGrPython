from sgr_library.payload_decoder import PayloadDecoder, PayloadBuilder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient


# In this case establishes a connection with the localhost server that is running the simulation.
class ModbusConnect:

    def __init__(self, ip: str, port: str):
        """
        Creates client with ip and port.
        """
        #EXAMPLE: client = ModbusTcpClient('127.0.0.1', 5002)
        self.client = ModbusTcpClient(ip, port)
        self.client.connect() #TODO a wrapper that opens and closes connection when function is excecuted?

    def value_decoder(self, addr: int, size: int, reg_type: str) -> float:
        """
        Reads register and decodes value
        :return: The float value
        """
        reg = self.client.read_holding_registers(addr, count=size)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        
        if not reg.isError():
            return decoder.decode(reg_type, 0)

    def value_encoder(self, addr: int, value: float, reg_type: str):
        """
        Encodes value to be set on the register address
        """
        builder = PayloadBuilder(byteorder=Endian.Little, wordorder=Endian.Little)
        builder.encode(value, reg_type, rounding="floor")
        self.client.write_registers(address=addr, values=builder.to_registers(), unit=0)
