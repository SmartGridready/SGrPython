import asyncio

from sgr_library.device_builder import DeviceBuilder


def test_loop():
    config_file = "config_wago"
    interface_file = "abb_terra_01.xml"

    config_file = "config_CLEMAPEnMon_ressource_default.ini"
    interface_file = "SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml"

    builder = DeviceBuilder()
    device = (
        builder.eid_path(interface_file).properties_path(config_file).build()
    )
    device.connect()

    vals = device.get_value()
    print(vals)

if __name__ == '__main__':
    try:
        test_loop()
    except KeyboardInterrupt:
        # Here we have to close all the sessions...
        # We have to think if we want to open a connection and close it for
        # every getval, or we just leave the user do this.
        print("done")
