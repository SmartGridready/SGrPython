import logging
import os
import time

from sgr_commhandler.device_builder import DeviceBuilder

logging.basicConfig(level=logging.DEBUG)

do_loop = False

def run_test_loop():
    print("start loop")

    current_dir = os.path.dirname(os.path.realpath(__file__))

    # --- REST ---

    # instantiate a REST device interface with a REST-API EID XML file
    eid_file = os.path.join(
        current_dir, "eid", "SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml"
    )
    ini_file = os.path.join(
        current_dir,
        "ini",
        "SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1_example.ini"
    )
    device = (
        DeviceBuilder()
        .eid_path(eid_file)
        .properties_path(ini_file)
        .build()
    )

    # connect to the REST device - also authenticate
    device.connect()

    # get all data point values once
    device.get_values()

    # create a loop where we request a data point value from the REST API
    while do_loop:
        # get data point from device and use get_value() to read value
        dp_val = device.get_data_point(
            ("ActivePowerAC", "ActivePowerACtot")
        ).get_value()
        print(dp_val)

        time.sleep(5)


if __name__ == "__main__":
    try:
        do_loop = True
        run_test_loop()
    except KeyboardInterrupt:
        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        do_loop = False
        print("done")
