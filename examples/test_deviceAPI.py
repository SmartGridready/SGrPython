
from sgr_library import SGrDevice
import asyncio


async def test_loop():

    config_file = 'config_wago'
    interface_file = 'abb_terra_01.xml'

    config_file = 'config_CLEMAPEnMon_ressource_default.ini'
    interface_file = 'SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml'

    

    device = SGrDevice()
    device.update_xml_spec(interface_file).update_config(config_file).build()
    await device.connect()

    #device_data = await device.read_data()
    #print(device_data)

    fp = device.get_function_profile("PowerFactor") #PowerFactor #VoltageAC
    #fp_data = await fp.read()
    #print(fp_data)

    dp = fp.get_data_point("PowerFactorTOT") #PowerFactorTOT #VoltageACL1
    dp_data = await dp.read()
    print(dp_data)

#VoltageDC_IN_1
#VoltageDC
#SGr_04_0014_0000_WAGO_Testsystem_V1.0.xml

try:
    asyncio.run(test_loop())
except KeyboardInterrupt:

    # Here we have to close all the sessions...
    # We have to think if we want to open a connection and close it for
    # every getval, or we just leave the user do this.
    print("done")