from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.data_point import DataPointBase
from sgrspecification.generic.functional_profile import FunctionalProfileBase
from sgrspecification.product.modbus_types import (
    ModbusAttributes,
    ModbusDataPointConfiguration,
    ModbusInterfaceDescription,
    TimeSyncBlockNotification,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class ModbusDataPoint(DataPointBase):
    """
    :ivar modbus_data_point_configuration:
    :ivar block_cache_identification: Refers to a
        timeSyncBlockNotification
    :ivar modbus_attributes:
    """
    modbus_data_point_configuration: Optional[ModbusDataPointConfiguration] = field(
        default=None,
        metadata={
            "name": "modbusDataPointConfiguration",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    block_cache_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "blockCacheIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    modbus_attributes: Optional[ModbusAttributes] = field(
        default=None,
        metadata={
            "name": "modbusAttributes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ModbusDataPointList:
    """
    List of data points.
    """
    data_point_list_element: List[ModbusDataPoint] = field(
        default_factory=list,
        metadata={
            "name": "dataPointListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class ModbusFunctionalProfile(FunctionalProfileBase):
    modbus_attributes: Optional[ModbusAttributes] = field(
        default=None,
        metadata={
            "name": "modbusAttributes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    data_point_list: Optional[ModbusDataPointList] = field(
        default=None,
        metadata={
            "name": "dataPointList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class ModbusFunctionalProfileList:
    """
    List of functional profiles.
    """
    functional_profile_list_element: List[ModbusFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "functionalProfileListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class ModbusInterface:
    """
    Container for a modbus device.
    """
    modbus_interface_description: Optional[ModbusInterfaceDescription] = field(
        default=None,
        metadata={
            "name": "modbusInterfaceDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    modbus_attributes: Optional[ModbusAttributes] = field(
        default=None,
        metadata={
            "name": "modbusAttributes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    functional_profile_list: Optional[ModbusFunctionalProfileList] = field(
        default=None,
        metadata={
            "name": "functionalProfileList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    time_sync_block_notification: List[TimeSyncBlockNotification] = field(
        default_factory=list,
        metadata={
            "name": "timeSyncBlockNotification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
