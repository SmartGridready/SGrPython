from xml.dom.minidom import Element
from modbus_interface import SgrModbusInterface
from restapi_interface import RestapiInterface
import os
import configparser
import xml.etree.ElementTree as ET
import asyncio


def get_protocol(xml_file:str) -> str:
    """
    Searches for protocol type in xml file
    :return: 
    """
    root = ET.parse(xml_file).getroot()
    element = root.tag
    protocol_type = element.split('}')[1]
    return protocol_type


class GenericInterface:


    def __new__(cls, xml_file:str, config_file=None):
        protocol_type = get_protocol(xml_file)
        modbus_protocol = ['SGrModbusDeviceFrame', 'SGrModbusDeviceDescriptionType']
        restapi_protocol = ['SGrRESTAPIDeviceDescriptionType', 'SGrRestAPIDeviceFrame']

        if protocol_type in modbus_protocol:
            obj = object.__new__(SgrModbusInterface)
            obj.__init__(xml_file)
            return obj
        elif protocol_type in restapi_protocol:
            obj = object.__new__(RestapiInterface)
            obj.__init__(xml_file, config_file)
            return obj
        return None

    """def __init__(self, xml_file: str, config_file=None) -> None:

        self.protocol_type = get_protocol(xml_file)
        self.modbus_protocol = ['SGrModbusDeviceFrame', 'SGrModbusDeviceDescriptionType']
        self.restapi_protocol = ['SGrRESTAPIDeviceDescriptionType']

        if self.protocol_type in self.modbus_protocol:
            SgrModbusInterface.__init__(self, xml_file) # Maybe add config file, but we just ignore it.
        elif self.protocol_type in self.restapi_protocol:
            RestapiInterface.__init__(self, xml_file, config_file)

    # Here we would wait asynchronously with PxPy (Reactive Programming).
    def getval(self, *parameter) -> tuple:
        if self.protocol_type in self.modbus_protocol:
            # Here we would wait asynchronously for the machine to answer.
            return(SgrModbusInterface.getval(self, *parameter)) 
        elif self.protocol_type in self.restapi_protocol:
            # Here we would wait asynchronously for the machine to answer.
            return(RestapiInterface.getval(self, *parameter))"""
        

if __name__ == "__main__":

    async def test_loop():
        while True:
            print('start')
            interface_file = 'SGr_04_0016_xxxx_ABBMeterV0.2.1.xml'
            client = GenericInterface(interface_file)
            await client.client.client.connect()
            getval = await client.getval('ActiveEnerBalanceAC', 'ActiveImportAC')
            print(getval)

            energy_monitor_config_file_path_default = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 
                'config_CLEMAPEnMon_ressource_default.ini'
                )
            config_file = configparser.ConfigParser()
            config_file.read(energy_monitor_config_file_path_default)

            interface_file = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
            sgr_component = GenericInterface(interface_file, config_file)
            value = sgr_component.getval('ActivePowerAC', 'ActivePowerACtot')
            print(value)

            await asyncio.sleep(10)

    asyncio.run(test_loop())

    

