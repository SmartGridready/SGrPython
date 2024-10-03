import asyncio
import os
from sgr_commhandler.api.device_builder import DeviceBuilder

if __name__ == "__main__":

    async def test_loop():

        print('start loop')

        # We instanciate one interface object with a modbus xml.
        interface_file_modbus = 'xml/abb_terra_01.xml'
        builder = DeviceBuilder()
        modbus_component = builder \
                            .eid_path(interface_file_modbus) \
                            .properties({}) \
                            .build()


        # We connect to the modbus component. # TODO fix connect thingy
        await modbus_component.connect_async()

        await modbus_component.get_value_async()
        # We instanciate an interface object with a restapi xml.
        config_file_rest = 'config_CLEMAPEnMon_ressource_default.ini'
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file_rest)

        # We instanciate a second interface object with a modbusTCP xml.

        # We authentificate the restapi conneciton

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
