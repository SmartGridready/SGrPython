import asyncio

from sgr_library.payload_decoder import PayloadDecoder, PayloadBuilder
from pymodbus.constants import Endian
from pymodbus.client import AsyncModbusSerialClient, ModbusSerialClient


# In this case establishes a connection with the localhost server that is running the simulation.

class SGrModbusRTUClient:

    def __init__(self, port: str, parity: str, baudrate: int, client=None):
        """
        Creates client
        :param ip: The host to connect to (default 127.0.0.1)
        :param port: The modbus port to connect to (default 502)
        """
        self._port = port
        if client is not None:
            self.client = client
        else:
            self.client = AsyncModbusSerialClient(
                method="rtu",
                port=port,
                parity=parity,
                baudrate=baudrate,
            )  # changed source: https://stackoverflow.com/questions/58773476/why-do-i-get-pymodbus-modbusioexception-on-20-of-attempts

            # connected = self.client.connect() #TODO a wrapper that opens and closes connection when function is excecuted?
            # if connected:
            #     print("Connected to ModbusRTU ond Port: " + port)

    async def connect(self):
        await self.client.connect()
        print("Connected to ModbusRTU ond Port: " + self._port)

    # not changed
    async def value_decoder(self, addr: int, size: int, data_type: str, register_type: str, slave_id: int,
                            order: Endian) -> float:
        """
        Reads register and decodes the value.
        :param addr: The address to read from and decode
        :param size: The number of registers to read
        :param data_type: The modbus type to decode
        :returns: Decoded float
        """
        if register_type == "HoldRegister":  # Todo im Modbus_client ist "HoldingRegister" angeben, ist das falsch?
            reg = await self.client.read_holding_registers(addr, count=size, slave=slave_id)
            # print(reg.registers)
        else:
            reg = await self.client.read_input_registers(addr, count=size, slave=slave_id)
        decoder = PayloadDecoder.fromRegisters(reg.registers, byteorder=order, wordorder=order)

        if not reg.isError():
            return decoder.decode(data_type, 0)

    # not changed
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


if __name__ == "__main__":
    async def run():
        MyClient = SGrModbusRTUClient("COM5", "E", 19200)

        connected = await MyClient.client.connect()

        a = await MyClient.value_decoder(0x5B14, 2, "int32", "HoldRegister", slave_id=1, order=Endian.Big)
        print(f"Der Wert ist: {a}")
        await MyClient.client.close()


    asyncio.run(run())
