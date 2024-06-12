from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from sgrspecification.generic.base_type_level_of_operation_type import LevelOfOperation
from sgrspecification.generic.base_types import (
    AlternativeNames,
    GenericAttributeListFunctionalProfile,
    LegibleDescription,
    ReleaseNotes,
)
from sgrspecification.product.modbus_types import ModbusInterfaceSelection
from sgrspecification.product.rest_api_types import RestApiInterfaceSelection

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class CommunicatorCategory(Enum):
    """
    Communicator types, a growing list of supported Communicators.
    """
    SMART_HOME = "SmartHome"
    LIGHT_CONTROL = "LightControl"
    POWER_BALANCER = "PowerBalancer"
    ACCOUNTING_SYSTEM = "AccountingSystem"


@dataclass
class CommunicatorTransportService:
    modbus: Optional[ModbusInterfaceSelection] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest: Optional[RestApiInterfaceSelection] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class TransportServices:
    """
    A list of supported transport services.
    """
    transport_service: List[CommunicatorTransportService] = field(
        default_factory=list,
        metadata={
            "name": "transportService",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class CommunicatorInformation:
    """
    :ivar alternative_names:
    :ivar legible_description: Published and printable information
        related to this communicator
    :ivar supported_transport_services:
    :ivar communicator_category:
    :ivar version_number:
    :ivar brand_name: branding information
    :ivar manufacturer_specification_identification: specification
        identifier
    :ivar manufacturer_label: the label of the device
    :ivar general_remarks: author of this sheet may add remarks / non
        disclaimer statements
    :ivar level_of_operation: defines the SGr Label Level 1...6 of the
        highest level functional profile supported by the communicator
    :ivar is_local_control: Value "false" means "is cloud control
        device", indicating that this service is based on cloud. "True"
        indicates that services are provided within the range of the
        local area.
    """
    alternative_names: Optional[AlternativeNames] = field(
        default=None,
        metadata={
            "name": "alternativeNames",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    legible_description: List[LegibleDescription] = field(
        default_factory=list,
        metadata={
            "name": "legibleDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    supported_transport_services: Optional[TransportServices] = field(
        default=None,
        metadata={
            "name": "supportedTransportServices",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    communicator_category: Optional[CommunicatorCategory] = field(
        default=None,
        metadata={
            "name": "communicatorCategory",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    version_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "versionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    brand_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "brandName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    manufacturer_specification_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufacturerSpecificationIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    manufacturer_label: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufacturerLabel",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    general_remarks: Optional[str] = field(
        default=None,
        metadata={
            "name": "generalRemarks",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    level_of_operation: Optional[LevelOfOperation] = field(
        default=None,
        metadata={
            "name": "levelOfOperation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    is_local_control: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isLocalControl",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class CommunicatorBase:
    """
    Base type for device.

    :ivar communicator_name: Device Name in the context of the
        manufacturer
    :ivar manufacturer_name: Name of the Manufacturer or OEM
    :ivar release_notes:
    :ivar specification_owner_identification: the identifier as
        enumeration indicates that the manufacturer is related with the
        organisation and that this declaration is generated by himself
    :ivar communicator_information:
    :ivar generic_attribute_list:
    """
    communicator_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "communicatorName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    manufacturer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufacturerName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    release_notes: Optional[ReleaseNotes] = field(
        default=None,
        metadata={
            "name": "releaseNotes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    specification_owner_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "specificationOwnerIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    communicator_information: Optional[CommunicatorInformation] = field(
        default=None,
        metadata={
            "name": "communicatorInformation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    generic_attribute_list: Optional[GenericAttributeListFunctionalProfile] = field(
        default=None,
        metadata={
            "name": "genericAttributeList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
