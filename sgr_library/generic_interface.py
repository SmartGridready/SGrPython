from modbus_interface import SgrModbusInterface
from restapi_client_async import SgrRestInterface

import asyncio
from auxiliary_functions import get_protocol


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
            obj = object.__new__(SgrRestInterface)
            obj.__init__(xml_file, config_file)
            return obj
        return None

        
if __name__ == "__main__":

    async def test_loop():

        print('start loop')

        # We instanciate one interface object with a modbus xml.
        interface_file_modbus = 'SGr_04_0016_xxxx_ABBMeterV0.2.1.xml'
        modbus_component = GenericInterface(interface_file_modbus)

        #TODO fix this ugly client.client.client.
        await modbus_component.client.client.connect()

        # We instanciate a second interface object with a restapi xml.
        config_file_rest = 'config_CLEMAPEnMon_ressource_default.ini'
        interface_file_rest = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
        restapi_component = GenericInterface(interface_file_rest, config_file_rest)
        await restapi_component.authenticate()

        # We create a loop where we request a datapoint with a getval of our restapi 
        # component and a datapoint with a getval of our modbus component.
        while True:
            
            getval = await modbus_component.getval('ActiveEnerBalanceAC', 'ActiveImportAC')
            print(getval)
            value = await restapi_component.getval('ActivePowerAC', 'ActivePowerACtot')
            print(value)
            await asyncio.sleep(10)

            #you could do the same funciton with a asyncio gather functions if you 
            #want to get the variables "concurrently".

    try:
        asyncio.run(test_loop())
    except KeyboardInterrupt:

        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        print("done")

