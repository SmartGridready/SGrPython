from sgr_library.generic_interface import GenericInterface, GenericSGrDeviceBuilder
import asyncio
import os

if __name__ == "__main__":

    async def test_loop():

        print('start loop')

        # We instanciate one interface object with a modbus xml.
        interface_file_modbus = 'xml/abb_terra_01.xml'
        builder = GenericSGrDeviceBuilder()
        modbus_component = builder \
                            .xml_file_path(interface_file_modbus) \
                            .config({}) \
                            .build()


        # We connect to the modbus component. # TODO fix connect thingy
        await modbus_component.connect_async()

        # We instanciate an interface object with a restapi xml.
        config_file_rest = 'config_CLEMAPEnMon_ressource_default.ini'
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file_rest)

        # We instanciate a second interface object with a modbusTCP xml.
        interface_file_rest = 'xml/SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml'
        restapi_component = GenericInterface(interface_file_rest, config_file_path)

        # We authentificate the restapi conneciton
        await restapi_component.authenticate()

        # We create a loop where we request a datapoint with a getval of our restapi
        # component and a datapoint with a getval of our modbus component.
        while True:
            # instanciate modbus component and use getval to get a value back.
            getval = await modbus_component.getval('CurrentAC', 'CurrentACL1')
            print(getval)

            # instanciate restapi component
            value = await restapi_component.getval('ActivePowerAC', 'ActivePowerACtot')
            print(value)

            await asyncio.sleep(1)

            # you could do the same funciton with a asyncio gather functions if you
            # want to get the variables "concurrently".


    try:
        asyncio.run(test_loop())
    except KeyboardInterrupt:

        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        print("done")
