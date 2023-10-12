from modbus_interface import SgrModbusInterface
from restapi_client_async import SgrRestInterface
import os

import asyncio
from auxiliary_functions import get_protocol, get_modbusInterfaceSelection
from sgr_library.modbusRTU_interface_async import SgrModbusRtuInterface


class GenericInterface:

    def __new__(cls, xml_file: str, config_file=None):
        if not os.path.exists(xml_file):
            raise FileNotFoundError(f"The specified XML file does not exist: {xml_file}")

        try:
            protocol_type = get_protocol(xml_file)
        except Exception as e:
            raise Exception(f"Error in getting protocol from XML: {e}")

        if protocol_type == "modbus":
            try:
                modbus_protocol_type = get_modbusInterfaceSelection(xml_file)
            except Exception as e:
                raise Exception(f"Error in getting Modbus interface selection: {e}")

            if modbus_protocol_type == "TCPIP":
                obj = object.__new__(SgrModbusInterface)
                obj.__init__(xml_file)
            elif modbus_protocol_type == "RTU":
                obj = object.__new__(SgrModbusRtuInterface)
                obj.__init__(xml_file)
            else:
                raise ValueError(f"Unsupported Modbus protocol type: {modbus_protocol_type}")
            return obj
            
        elif protocol_type == "restapi":
            obj = object.__new__(SgrRestInterface)
            obj.__init__(xml_file, config_file)
            return obj
            
        else:
            raise ValueError(f"Unsupported protocol type: {protocol_type}")

        
if __name__ == "__main__":

    async def test_loop():

        print('start loop')

        # We instanciate one interface object with a modbus xml.
        interface_file_modbus = 'abb_terra_01.xml'
        modbus_component = GenericInterface(interface_file_modbus)

        # We connect to the modbus component. # TODO fix connect thingy
        await modbus_component.connect()

        # We instanciate a second interface object with a restapi xml.
        config_file_rest = 'config_CLEMAPEnMon_ressource_default.ini'

        #interface_file_rest = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
        interface_file_rest = 'SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml'
        restapi_component = GenericInterface(interface_file_rest, config_file_rest)

        # We authentificate the restapi conneciton
        await restapi_component.authenticate()

        # We create a loop where we request a datapoint with a getval of our restapi 
        # component and a datapoint with a getval of our modbus component.
        while True:

            # instanciate modbus component
            """getval = await modbus_component.getval('ActiveEnerBalanceAC', 'ActiveImportAC')
            print(getval)"""

            # instanciate restapi component
            value = await restapi_component.getval('ActivePowerAC', 'ActivePowerACtot')
            print(value)

            await asyncio.sleep(1)

            #you could do the same funciton with a asyncio gather functions if you 
            #want to get the variables "concurrently".

    try:
        asyncio.run(test_loop())
    except KeyboardInterrupt:

        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        print("done")

