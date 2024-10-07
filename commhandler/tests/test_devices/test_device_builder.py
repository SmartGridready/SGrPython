import os
from sgr_commhandler.device_builder import (
    DeviceBuilder
)


EID_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'eids')
INI_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ini')


def test_device_builder_modbus_tcp_dict():
    eid_path = os.path.join(EID_BASE_PATH, 'SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.3.xml')
    eid_properties = dict(
        tcp_address='127.0.0.1',
        tcp_port='502'
    )

    test_device = DeviceBuilder().eid_path(eid_path).properties(eid_properties).build()
    assert test_device is not None

    device_info = test_device.device_information()
    assert device_info is not None
    assert device_info.manufacture == 'ABB'
    assert device_info.name == 'betaABBMeterTcpV0.3.0'


def test_device_builder_modbus_tcp_ini():
    eid_path = os.path.join(EID_BASE_PATH, 'SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.3.xml')
    eid_properties_path = os.path.join(INI_BASE_PATH, 'SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.3.ini')

    test_device = DeviceBuilder().eid_path(eid_path).properties_path(eid_properties_path).build()
    assert test_device is not None

    device_info = test_device.device_information()
    assert device_info is not None
    assert device_info.manufacture == 'ABB'
    assert device_info.name == 'betaABBMeterTcpV0.3.0'


def test_device_builder_rest_dict():
    eid_path = os.path.join(EID_BASE_PATH, 'SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.xml')
    eid_properties = dict(
        baseUri='http://127.0.0.1'
    )

    test_device = DeviceBuilder().eid_path(eid_path).properties(eid_properties).build()
    assert test_device is not None

    device_info = test_device.device_information()
    assert device_info is not None
    assert device_info.manufacture == 'Shelly'
    assert device_info.name == 'Shelly 1PM Local'


def test_device_builder_rest_ini():
    eid_path = os.path.join(EID_BASE_PATH, 'SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.xml')
    eid_properties_path = os.path.join(INI_BASE_PATH, 'SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.ini')

    test_device = DeviceBuilder().eid_path(eid_path).properties_path(eid_properties_path).build()
    assert test_device is not None

    device_info = test_device.device_information()
    assert device_info is not None
    assert device_info.manufacture == 'Shelly'
    assert device_info.name == 'Shelly 1PM Local'
