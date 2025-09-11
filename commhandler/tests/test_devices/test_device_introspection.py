import os

import pytest

from sgr_specification.v0.product import (
    DeviceFrame,
    ModbusFunctionalProfile as ModbusFunctionalProfileSpec,
    ModbusDataPoint as ModbusDataPointSpec
)
from sgr_commhandler.api.data_point_api import DataPoint
from sgr_commhandler.driver.modbus.modbus_interface_async import SGrModbusInterface, ModbusFunctionalProfile
from sgr_commhandler.device_builder import DeviceBuilder

EID_BASE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "eids"
)

def _load_device():
    eid_path = os.path.join(
        EID_BASE_PATH, "SGr_00_0016_dddd_ABB_B23_ModbusTCP_V0.4.xml"
    )
    eid_properties = dict(slave_id="1", tcp_address="127.0.0.1", tcp_port="502")
    return DeviceBuilder().eid_path(eid_path).properties(eid_properties).build()

@pytest.mark.asyncio
async def test_device_introspection_device():
    device = _load_device()
    assert device is not None
    assert isinstance(device, SGrModbusInterface)

    device_frame = device.get_specification()
    assert isinstance(device_frame, DeviceFrame)

@pytest.mark.asyncio
async def test_device_introspection_fp():
    device = _load_device()
    assert device is not None
    assert isinstance(device, SGrModbusInterface)

    fp = device.get_functional_profile("CurrentAC")
    assert isinstance(fp, ModbusFunctionalProfile)

    fp_frame = fp.get_specification()
    assert isinstance(fp_frame, ModbusFunctionalProfileSpec)

@pytest.mark.asyncio
async def test_device_introspection_dp():
    device = _load_device()
    assert device is not None
    assert isinstance(device, SGrModbusInterface)

    dp = device.get_data_point(("CurrentAC", "CurrentACL1"))
    assert isinstance(dp, DataPoint)

    dp_frame = dp.get_specification()
    assert isinstance(dp_frame, ModbusDataPointSpec)
