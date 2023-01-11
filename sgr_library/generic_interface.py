from xml.dom.minidom import Element
from modbus_interface import SgrModbusInterface
from restapi_client_async import RestapiConnect
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
            obj = object.__new__(RestapiConnect)
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

        print('start loop')

        # We instanciate one interface object with a modbus xml
        interface_file_modbus = 'SGr_04_0016_xxxx_ABBMeterV0.2.1.xml'
        client = GenericInterface(interface_file_modbus)

        #TODO fix this ugly client.client.client
        await client.client.client.connect()

        # We instanciate a second interface object with a restapi xml
        config_file_rest = 'config_CLEMAPEnMon_ressource_default.ini'
        interface_file_rest = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
        sgr_component = GenericInterface(interface_file_rest, config_file_rest)
        await sgr_component.authenticate()

        while True:
            
            getval = await client.getval('ActiveEnerBalanceAC', 'ActiveImportAC')
            print(getval)
            value = await sgr_component.getval('ActivePowerAC', 'ActivePowerACtot')
            print(value)
            await asyncio.sleep(10)

            #you could do the same funciton with a asyncio gather functions if you 
            #want to get the variables "concurrently"

    asyncio.run(test_loop())

    

