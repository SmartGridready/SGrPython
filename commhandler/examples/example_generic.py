import logging
import asyncio
import os
from sgr_commhandler.device_builder import DeviceBuilder


logging.basicConfig(level=logging.DEBUG)


async def run_test_loop():
    print("start loop")

    current_dir = os.path.dirname(os.path.realpath(__file__))

    # --- Modbus ---

    # We instantiate a Modbus device interface with a Modbus EID XML file
    eid_file_modbus = os.path.join(current_dir, "eid", "abb_terra_01.xml")
    ini_file_modbus = os.path.join(current_dir, "ini", "abb_terra_01_example.ini")
    modbus_device = (
        DeviceBuilder()
        .eid_path(eid_file_modbus)
        .properties_path(ini_file_modbus)
        .build()
    )

    # We connect to the Modbus device
    await modbus_device.connect_async()

    await modbus_device.get_values_async()

    # --- REST ---

    # We instantiate a REST device interface with a REST-API EID XML file
    eid_file_rest = os.path.join(
        current_dir, "eid", "SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml"
    )
    ini_file_rest = os.path.join(
        current_dir, "ini", "SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1_example.ini"
    )
    rest_device = (
        DeviceBuilder().eid_path(eid_file_rest).properties_path(ini_file_rest).build()
    )

    # We connect to the REST device
    await rest_device.connect_async()

    await rest_device.get_values_async()

    # We create a loop where we request a datapoint with a getval of our restapi
    # component and a datapoint with a getval of our modbus component.
    while True:
        # instanciate modbus component and use getval to get a value back.
        modbus_val = await modbus_device.get_data_point(
            ("CurrentAC", "CurrentACL1")
        ).get_value_async()
        print(modbus_val)

        # instanciate restapi component
        rest_val = await rest_device.get_data_point(
            ("ActivePowerAC", "ActivePowerACtot")
        ).get_value_async()
        print(rest_val)

        await asyncio.sleep(1)

        # you could do the same funciton with a asyncio gather functions if you
        # want to get the variables "concurrently".


if __name__ == "__main__":
    try:
        asyncio.run(run_test_loop())
    except KeyboardInterrupt:
        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        print("done")
