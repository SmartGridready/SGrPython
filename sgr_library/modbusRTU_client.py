from sgr_library.payload_decoder import PayloadDecoder, PayloadBuilder
from pymodbus.constants import Endian
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from sgr_library.modbus_interface import SgrModbusInterface

# In this case establishes a connection with the localhost server that is running the simulation.

class SGrModbusRTUClient:

    def __init__(self, port: str, parity: str, baudrate: int):
        """
        Creates client
        :param ip: The host to connect to (default 127.0.0.1)
        :param port: The modbus port to connect to (default 502)
        """
        #EXAMPLE: client = ModbusTcpClient('127.0.0.1', 5002)
        self.client = ModbusSerialClient(method="rtu", port=port, parity=parity, baudrate=baudrate, timeout=1) #changed source: https://stackoverflow.com/questions/58773476/why-do-i-get-pymodbus-modbusioexception-on-20-of-attempts
        connected = self.client.connect() #TODO a wrapper that opens and closes connection when function is excecuted?
        if connected:
            print("Connected to ModbusRTU ond Port: " + port)

    #not changed
    def value_decoder(self, addr: int, size: int, data_type: str, register_type: str, slave_id: int, order: Endian) -> float:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        if register_type == "HoldRegister": #Todo im Modbus_client ist "HoldingRegister" angeben, ist das falsch?
            reg = self.client.read_holding_registers(addr, count=size, unit=slave_id)
            #print(reg.registers)
        else:
            reg = self.client.read_input_registers(addr, count=size, unit=slave_id)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=order, wordorder=order)
        
        if not reg.isError():
            return decoder.decode(data_type, 0)
    #not changed
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

if __name__ == "__main__":


    #Build Connection
    myRTUModbus = SGrModbusRTUClient("COM7", "E", 19200)

    #int16_u --> 16bit pro register, signedvalue
    Power = myRTUModbus.value_decoder(0x5B14,2,"int32","HoldingRegister",1,Endian.Big)

    print(str(Power*0.01) + "W")

    myRTUModbus.client.close()
    print("finished")

    """
    # Create interface instance
    interface_file = '../xml_files/SGr_04_0016_xxxx_ABBMeterV0.2.1_edited_S.Ferreira.xml'
    sgr_component = SgrModbusInterface(interface_file)

    x = sgr_component.getval("ActiveEnerBalanceAC","ActiveImportAC")

    print(x)
    """
