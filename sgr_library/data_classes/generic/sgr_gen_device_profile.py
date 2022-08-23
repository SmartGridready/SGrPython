from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from sgr_library.data_classes.generic.sgr_gen_type_definitions import (
    SgrDeviceKindType,
    SgrLegibDocumentationType,
    SgrNamelistType,
    SgrPowerSourceType,
    SgrVersionNumberType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class SgrTransportServicesUsedListType(Enum):
    EEBUS = "EEBUS"
    MODBUS = "Modbus"
    OCPP1_6 = "OCPP1.6"
    OCPP2_01 = "OCPP2.01"
    RESTFUL_JSON = "RESTfulJSON"
    CONTACTS = "Contacts"
    WO_T = "WoT"
    PROPRIETARY = "proprietary"
    GENERIC = "generic"


@dataclass
class SgrDeviceProfileType:
    """
    :ivar dev_name_list: Ontology naming support
    :ivar dev_legib_desc: this is the published information related to
        this device
    :ivar transport_service:
    :ivar device_kind:
    :ivar serial_number:
    :ivar software_revision:
    :ivar hardware_revision:
    :ivar brand_name: branding information
    :ivar power_source: power supply type
    :ivar nominal_power: nominal Power of the device (installation)
    :ivar manuf_spec_ident: specififaction identifier
    :ivar manufacturer_label: the label of the device
    :ivar rem_author_id: author of this sheet may add remarks / non
        disclamer statements
    :ivar dev_levelof_operation: defines the SGr Label Leve 1...6 of the
        highest level functional profile of this device
    :ivar dev_prg_desc:
    """
    class Meta:
        name = "SGrDeviceProfileType"

    dev_name_list: Optional[SgrNamelistType] = field(
        default=None,
        metadata={
            "name": "devNameList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dev_legib_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "devLegibDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    transport_service: Optional[SgrTransportServicesUsedListType] = field(
        default=None,
        metadata={
            "name": "transportService",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    device_kind: Optional[SgrDeviceKindType] = field(
        default=None,
        metadata={
            "name": "deviceKind",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    serial_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "serialNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    software_revision: Optional[SgrVersionNumberType] = field(
        default=None,
        metadata={
            "name": "softwareRevision",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    hardware_revision: Optional[SgrVersionNumberType] = field(
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
    power_source: Optional[SgrPowerSourceType] = field(
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
    manuf_spec_ident: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufSpecIdent",
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
    rem_author_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "remAuthorID ",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dev_levelof_operation: Optional[int] = field(
        default=None,
        metadata={
            "name": "devLevelofOperation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dev_prg_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "devPrgDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )


@dataclass
class SgrInterfaceDescriptionType:
    class Meta:
        name = "SGrInterfaceDescriptionType"

    technology_used: Optional[SgrTransportServicesUsedListType] = field(
        default=None,
        metadata={
            "name": "technologyUsed",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    is_local_control: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsLocalControl",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class DeviceProfile(SgrDeviceProfileType):
    class Meta:
        namespace = "http://www.smartgridready.com/ns/V0/"
