from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.ei_modbus.sgr_modbus_eiconfigurator import (
    SgrAttr4ModbusType,
    SgrModbusDataPointDescriptionType,
    SgrModbusInterfaceDescriptionType,
)
from data_classes.ei_modbus.sgr_modbus_helpers import NetworkConnectionStateType
from data_classes.generic.sgr_base_device_frame import (
    SgrDataPointBaseType,
    SgrDeviceBaseType,
    SgrFunctionalProfileBaseType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrModbusDataPointType(SgrDataPointBaseType):
    """
    Extends the base data point type with Modbus attributes and data points.
    """
    class Meta:
        name = "SGrModbusDataPointType"

    modbus_data_point: List[SgrModbusDataPointDescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "modbusDataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    modbus_attr: List[SgrAttr4ModbusType] = field(
        default_factory=list,
        metadata={
            "name": "modbusAttr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrModbusFunctionalProfileType(SgrFunctionalProfileBaseType):
    """
    Extends the base functional profile type with Modbus attributes and data
    points.
    """
    class Meta:
        name = "SGrModbusFunctionalProfileType"

    modbus_attr: Optional[SgrAttr4ModbusType] = field(
        default=None,
        metadata={
            "name": "modbusAttr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_list_element: List[SgrModbusDataPointType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrModbusDeviceFrame(SgrDeviceBaseType):
    """
    RPT Root Point for Modbux Device External Interface.
    """
    class Meta:
        name = "SGrModbusDeviceFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"

    modbus_attr: Optional[SgrAttr4ModbusType] = field(
        default=None,
        metadata={
            "name": "modbusAttr",
            "type": "Element",
        }
    )
    modbus_interface_desc: Optional[SgrModbusInterfaceDescriptionType] = field(
        default=None,
        metadata={
            "name": "modbusInterfaceDesc",
            "type": "Element",
            "required": True,
        }
    )
    fp_list_element: List[SgrModbusFunctionalProfileType] = field(
        default_factory=list,
        metadata={
            "name": "fpListElement",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    network_connection_state: Optional[NetworkConnectionStateType] = field(
        default=None,
        metadata={
            "name": "networkConnectionState",
            "type": "Element",
        }
    )
