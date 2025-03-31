import asyncio
import logging
import os

from sgr_commhandler.device_builder import DeviceBuilder

logging.basicConfig(level=logging.DEBUG)

do_loop = False

async def run_test_loop():
    print("start loop")

    current_dir = os.path.dirname(os.path.realpath(__file__))

    # --- Modbus ---

    # instantiate a Modbus device interface with a Modbus EID XML file
    eid_file = os.path.join(
        current_dir, "eid", "abb_terra_01.xml"
    )
    ini_file = os.path.join(
        current_dir,
        "ini",
        "abb_terra_01_example.ini"
    )
    device = (
        DeviceBuilder()
        .eid_path(eid_file)
        .properties_path(ini_file)
        .build()
    )

    # connect to the Modbus device
    await device.connect_async()

    # get all data point values once
    await device.get_values_async()

    # create a loop where we request a data point value from the Modbus interface
    while do_loop:
        # get data point from device and use get_value_async() to read value
        dp_val = await device.get_data_point(
            ("CurrentAC", "CurrentACL1")
        ).get_value_async()
        print(dp_val)

        await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        do_loop = True
        asyncio.run(run_test_loop())
    except KeyboardInterrupt:
        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        do_loop = False
        print("done")
