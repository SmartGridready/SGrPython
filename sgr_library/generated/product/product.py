from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.base_type_level_of_operation_type import LevelOfOperation
from sgrspecification.generic.base_types import (
    AlternativeNames,
    DataTypeProduct,
    DeviceCategory,
    GenericAttributeListProduct,
    LegibleDescription,
    PowerSource,
    ReleaseNotes,
    VersionNumber,
)
from sgrspecification.product.contact_interface import ContactInterface
from sgrspecification.product.generic_interface import GenericInterface
from sgrspecification.product.modbus_interface import ModbusInterface
from sgrspecification.product.rest_api_interface import RestApiInterface

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class ConfigurationDescription(LegibleDescription):
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class DeviceInformation:
    """
    :ivar alternative_names:
    :ivar legible_description: Published and printable information
        related to this product
    :ivar device_category:
    :ivar is_local_control: Value "false" means "is cloud control
        device", indicating that this service is based on cloud. "True"
        indicates that services are provided within the range of the
        local area.
    :ivar software_revision: software version information for this
        product declaration
    :ivar hardware_revision: hardware version information for this
        product declaration
    :ivar brand_name: branding information
    :ivar power_source: power supply type
    :ivar nominal_power: nominal Power of the device (installation)
    :ivar manufacturer_specification_identification: manufacturers
        specification identifier
    :ivar manufacturer_label: manufacturers label of the device
    :ivar general_remarks: author of this sheet may add remarks / non
        disclaimer statements
    :ivar level_of_operation: defines the SGr Label Level 1...6 of the
        highest level functional profile of this device
    :ivar version_number:
    :ivar programmer_hints: additional device-specific implementation
        hints for this device
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
    device_category: Optional[DeviceCategory] = field(
        default=None,
        metadata={
            "name": "deviceCategory",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
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
    software_revision: Optional[str] = field(
        default=None,
        metadata={
            "name": "softwareRevision",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    hardware_revision: Optional[str] = field(
        default=None,
        metadata={
            "name": "hardwareRevision",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
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
    power_source: Optional[PowerSource] = field(
        default=None,
        metadata={
            "name": "powerSource",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    nominal_power: Optional[str] = field(
        default=None,
        metadata={
            "name": "nominalPower",
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
    version_number: Optional[VersionNumber] = field(
        default=None,
        metadata={
            "name": "versionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    programmer_hints: List[LegibleDescription] = field(
        default_factory=list,
        metadata={
            "name": "programmerHints",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )


@dataclass
class InterfaceList:
    """
    List of supported interfaces.
    """
    modbus_interface: Optional[ModbusInterface] = field(
        default=None,
        metadata={
            "name": "modbusInterface",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_api_interface: Optional[RestApiInterface] = field(
        default=None,
        metadata={
            "name": "restApiInterface",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    contact_interface: Optional[ContactInterface] = field(
        default=None,
        metadata={
            "name": "contactInterface",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    generic_interface: Optional[GenericInterface] = field(
        default=None,
        metadata={
            "name": "genericInterface",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ConfigurationListElement:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    data_type: Optional[DataTypeProduct] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    configuration_description: List[ConfigurationDescription] = field(
        default_factory=list,
        metadata={
            "name": "configurationDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )


@dataclass
class ConfigurationList:
    configuration_list_element: List[ConfigurationListElement] = field(
        default_factory=list,
        metadata={
            "name": "configurationListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class DeviceFrame:
    """
    Product declaration.

    :ivar device_name: Device Name in the context of the manufacturer
    :ivar manufacturer_name: Name of the Manufacturer or OEM
    :ivar specification_owner_identification:
    :ivar release_notes:
    :ivar device_information:
    :ivar configuration_list:
    :ivar generic_attribute_list:
    :ivar interface_list:
    """
    class Meta:
        namespace = "http://www.smartgridready.com/ns/V0/"

    device_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceName",
            "type": "Element",
            "required": True,
        }
    )
    manufacturer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufacturerName",
            "type": "Element",
        }
    )
    specification_owner_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "specificationOwnerIdentification",
            "type": "Element",
            "required": True,
        }
    )
    release_notes: Optional[ReleaseNotes] = field(
        default=None,
        metadata={
            "name": "releaseNotes",
            "type": "Element",
            "required": True,
        }
    )
    device_information: Optional[DeviceInformation] = field(
        default=None,
        metadata={
            "name": "deviceInformation",
            "type": "Element",
            "required": True,
        }
    )
    configuration_list: Optional[ConfigurationList] = field(
        default=None,
        metadata={
            "name": "configurationList",
            "type": "Element",
        }
    )
    generic_attribute_list: Optional[GenericAttributeListProduct] = field(
        default=None,
        metadata={
            "name": "genericAttributeList",
            "type": "Element",
        }
    )
    interface_list: Optional[InterfaceList] = field(
        default=None,
        metadata={
            "name": "interfaceList",
            "type": "Element",
            "required": True,
        }
    )
