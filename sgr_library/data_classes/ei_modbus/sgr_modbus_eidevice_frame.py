from dataclasses import dataclass, field
from typing import List, Optional
from sgr_library.data_classes.ei_modbus.sgr_modbus_eiconfigurator import (
    SgrAccessProtectionEnabledType,
    SgrModbusDataPointDescriptionType,
    SgrModbusInterfaceDescriptionType,
)
from sgr_library.data_classes.ei_modbus.sgr_modbus_eidata_types import TimeSyncBlockNotificationType
from sgr_library.data_classes.ei_modbus.sgr_modbus_helpers import NetworkConnectionStateType
from sgr_library.data_classes.generic.sgr_gen_data_point_definition import SgrDataPointDescriptionType
from sgr_library.data_classes.generic.sgr_gen_device_profile import SgrDeviceProfileType
from sgr_library.data_classes.generic.sgr_gen_functional_profile_definition import SgrProfileDescriptionType
from sgr_library.data_classes.generic.sgr_gen_type_definitions import (
    SgrAttr4GenericType,
    SgrScalingType,
)
from sgr_library.data_classes.generic.sgr_manufacturer_list import SgrManufacturerIdtype

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrAttr4ModbusType:
    """
    Modbus Attributes support TransportService specific parameters.

    :ivar scaling_by_mul_pwr: generic value = dataPoint * m * 10^p
    :ivar step_by_increment: each didgit
    :ivar sunssf: a Sunpec specific attribute (scalefactor p -10 ...
        +10) generic value = dataPoint * 10^p note: Sunspec uses sunssf
        usually as Modbus Register with dynamic values check attribute
        "timeAlignedNotification"
    :ivar poll_latency_ms: the time for a master slave communication
        cycle in ms
    :ivar time_sync_block_notification: a transaction number for a
        sequence of Regsisteres (usually transmitted by Blocktransfers)
        to be transferred together
    :ivar access_protection:
    """
    class Meta:
        name = "SGrAttr4ModbusType"

    scaling_by_mul_pwr: Optional[SgrScalingType] = field(
        default=None,
        metadata={
            "name": "scalingByMulPwr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    step_by_increment: Optional[int] = field(
        default=None,
        metadata={
            "name": "stepByIncrement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sunssf: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    poll_latency_ms: Optional[int] = field(
        default=None,
        metadata={
            "name": "pollLatencyMS",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    time_sync_block_notification: Optional[TimeSyncBlockNotificationType] = field(
        default=None,
        metadata={
            "name": "timeSyncBlockNotification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    access_protection: Optional[SgrAccessProtectionEnabledType] = field(
        default=None,
        metadata={
            "name": "accessProtection",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrModbusAttrFrameType:
    class Meta:
        name = "SGrModbusAttrFrameType"

    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
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
class SgrModbusDataPointsFrameType:
    """RPT Root Point for stand alone Modbus Functional Profile description.

    It includes the embedded generic Porfile decription

    :ivar data_point:
    :ivar modbus_data_point: ModbusAttrFrameTypes contain two branches
        of SmartGridready attributes: Modbus related and Generic
        fpMbAttrRefernce values are valid for a single datapoint
    :ivar dp_mb_attr_reference:
    """
    class Meta:
        name = "SGrModbusDataPointsFrameType"

    data_point: List[SgrDataPointDescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "dataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    modbus_data_point: List[SgrModbusDataPointDescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "modbusDataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    dp_mb_attr_reference: List[SgrModbusAttrFrameType] = field(
        default_factory=list,
        metadata={
            "name": "dpMbAttrReference",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrModbusProfilesFrameType:
    """
    :ivar functional_profile:
    :ivar fp_mb_attr_reference: ModbusAttrFrameTypes contain two
        branches of SmartGridready attributes: Modbus related and
        Generic fpMbAttrRefernce values are valid for a whole functional
        profile
    :ivar dp_list_element:
    """
    class Meta:
        name = "SGrModbusProfilesFrameType"

    functional_profile: Optional[SgrProfileDescriptionType] = field(
        default=None,
        metadata={
            "name": "functionalProfile",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    fp_mb_attr_reference: List[SgrModbusAttrFrameType] = field(
        default_factory=list,
        metadata={
            "name": "fpMbAttrReference",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_list_element: List[SgrModbusDataPointsFrameType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrModbusDeviceDescriptionType:
    """
    Data Typde definition for a Modbus Device Description as an EI (External
    Interface) Geraet.

    :ivar device_profile:
    :ivar dev_mb_attr_reference: ModbusAttrFrameTypes contain two
        branches of SmartGridready attributes: Modbus related and
        Generic devMbAttrRefernce values are valid for a whole device
    :ivar modbus_interface_desc:
    :ivar fp_list_element:
    :ivar network_connection_state:
    :ivar device_name: Device Name in the context of the ManufacturerID
    :ivar manufacturer_name: Name of the Manufacturer or OEM
    :ivar manufacturer_id: the identifier as enumeration indicates that
        the manufacturer is related with the organisation and that this
        external interface is generated by himself
    :ivar is_local_control: Value "false" means "is cloud control
        device", indicating that this service is based on cloud. "True"
        indicates that services are provided within the range of the
        local area.
    """
    class Meta:
        name = "SGrModbusDeviceDescriptionType"
        namespace = "http://www.smartgridready.com/ns/V0/"

    device_profile: Optional[SgrDeviceProfileType] = field(
        default=None,
        metadata={
            "name": "deviceProfile",
            "type": "Element",
            "required": True,
        }
    )
    dev_mb_attr_reference: List[SgrModbusAttrFrameType] = field(
        default_factory=list,
        metadata={
            "name": "devMbAttrReference",
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
    fp_list_element: List[SgrModbusProfilesFrameType] = field(
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
    device_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceName",
            "type": "Attribute",
        }
    )
    manufacturer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufacturerName",
            "type": "Attribute",
        }
    )
    manufacturer_id: Optional[SgrManufacturerIdtype] = field(
        default=None,
        metadata={
            "name": "manufacturerID",
            "type": "Attribute",
        }
    )
    is_local_control: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isLocalControl",
            "type": "Attribute",
        }
    )


@dataclass
class SgrModbusDeviceFrame(SgrModbusDeviceDescriptionType):
    """RPT Root Point for stand alone Modbus Device description.

    It includes the embedded generic Device decription
    """
    class Meta:
        name = "SGrModbusDeviceFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"
