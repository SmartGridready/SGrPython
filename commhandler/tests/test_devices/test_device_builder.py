import os

import pytest

from sgr_commhandler.device_builder import DeviceBuilder

EID_BASE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "eids"
)
INI_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ini")


@pytest.mark.asyncio
async def test_device_builder_modbus_tcp_dict():
    eid_path = os.path.join(
        EID_BASE_PATH, "SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.4.xml"
    )
    eid_properties = dict(slave_id="1", tcp_address="127.0.0.1", tcp_port="502")

    test_device = (
        DeviceBuilder().eid_path(eid_path).properties(eid_properties).build()
    )
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "ABB"
    assert device_info.name == "ABB B23 TCP"

    device_frame = test_device.device_frame
    assert device_frame.interface_list.modbus_interface is not None
    assert device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.slave_id == '1'
    assert device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.address == '127.0.0.1'
    assert device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.port == '502'


@pytest.mark.asyncio
async def test_device_builder_modbus_tcp_ini():
    eid_path = os.path.join(
        EID_BASE_PATH, "SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.4.xml"
    )
    eid_properties_path = os.path.join(
        INI_BASE_PATH, "SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.4.ini"
    )

    test_device = (
        DeviceBuilder()
        .eid_path(eid_path)
        .properties_path(eid_properties_path)
        .build()
    )
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "ABB"
    assert device_info.name == "ABB B23 TCP"

    device_frame = test_device.device_frame
    assert device_frame.interface_list.modbus_interface is not None
    assert device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.slave_id == '1'
    assert device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.address == '127.0.0.1'
    assert device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.port == '502'


@pytest.mark.asyncio
async def test_device_builder_rest_dict():
    eid_path = os.path.join(
        EID_BASE_PATH, "SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.xml"
    )
    eid_properties = dict(base_uri="http://127.0.0.1")

    test_device = (
        DeviceBuilder().eid_path(eid_path).properties(eid_properties).build()
    )
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "Shelly"
    assert device_info.name == "Shelly 1PM Local"

    device_frame = test_device.device_frame
    assert device_frame.interface_list.rest_api_interface is not None
    assert device_frame.interface_list.rest_api_interface.rest_api_interface_description.rest_api_uri == 'http://127.0.0.1'


@pytest.mark.asyncio
async def test_device_builder_rest_ini():
    eid_path = os.path.join(
        EID_BASE_PATH, "SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.xml"
    )
    eid_properties_path = os.path.join(
        INI_BASE_PATH, "SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.ini"
    )

    test_device = (
        DeviceBuilder()
        .eid_path(eid_path)
        .properties_path(eid_properties_path)
        .build()
    )
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "Shelly"
    assert device_info.name == "Shelly 1PM Local"

    device_frame = test_device.device_frame
    assert device_frame.interface_list.rest_api_interface is not None
    assert device_frame.interface_list.rest_api_interface.rest_api_interface_description.rest_api_uri == 'http://127.0.0.1'


@pytest.mark.asyncio
async def test_device_builder_messaging_dict():
    eid_path = os.path.join(EID_BASE_PATH, "SGr_XX_HiveMQ_MQTT_Cloud.xml")
    eid_properties = dict(
        host="152f30e8c480481886072e4f8250d91a.s1.eu.hivemq.cloud",
        port="8883",
        username="smartgrid",
        password="1SmartGrid!",
    )

    test_device = (
        DeviceBuilder().eid_path(eid_path).properties(eid_properties).build()
    )
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "HiveMQ"
    assert device_info.name == "HiveMQ Test Cloud"

    device_frame = test_device.device_frame
    assert device_frame.interface_list.messaging_interface is not None
    assert device_frame.interface_list.messaging_interface.messaging_interface_description.message_broker_list.message_broker_list_element[0].host == '152f30e8c480481886072e4f8250d91a.s1.eu.hivemq.cloud'


@pytest.mark.asyncio
async def test_device_builder_messaging_ini():
    eid_path = os.path.join(EID_BASE_PATH, "SGr_XX_HiveMQ_MQTT_Cloud.xml")
    eid_properties_path = os.path.join(
        INI_BASE_PATH, "SGr_XX_HiveMQ_MQTT_Cloud.ini"
    )

    test_device = (
        DeviceBuilder()
        .eid_path(eid_path)
        .properties_path(eid_properties_path)
        .build()
    )
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "HiveMQ"
    assert device_info.name == "HiveMQ Test Cloud"

    device_frame = test_device.device_frame
    assert device_frame.interface_list.messaging_interface is not None
    assert device_frame.interface_list.messaging_interface.messaging_interface_description.message_broker_list.message_broker_list_element[0].host == '152f30e8c480481886072e4f8250d91a.s1.eu.hivemq.cloud'


@pytest.mark.asyncio
async def test_device_builder_contact_noprops():
    eid_path = os.path.join(EID_BASE_PATH, "test_eid_contacts_V0.1.xml")

    test_device = DeviceBuilder().eid_path(eid_path).build()
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "Test"
    # TODO is this an UTF-8 problem?
    assert device_info.name == "Test SGCP Contacts"


@pytest.mark.asyncio
async def test_device_builder_generic_noprops():
    eid_path = os.path.join(EID_BASE_PATH, "test_eid_generic_V0.1.xml")

    test_device = DeviceBuilder().eid_path(eid_path).build()
    assert test_device is not None

    device_info = test_device.device_information
    assert device_info is not None
    assert device_info.manufacturer == "Test"
    assert device_info.name == "Test Device Generic"
