from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.generic.sgr_gen_data_point_definition import SgrDataPointDescriptionType
from data_classes.generic.sgr_gen_device_profile import SgrDeviceProfileType
from data_classes.generic.sgr_gen_functional_profile_definition import SgrProfileDescriptionType
from data_classes.generic.sgr_gen_type_definitions import (
    SgrAttr4GenericType,
    SgrReleaseNotes,
)
from data_classes.generic.sgr_manufacturer_list import SgrManufacturerIdtype

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrDataPointsFrameType:
    class Meta:
        name = "SGrDataPointsFrameType"

    data_point: Optional[SgrDataPointDescriptionType] = field(
        default=None,
        metadata={
            "name": "dataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrProfilesFrameType:
    """
    Functional Profile description in generic lineup.
    """
    class Meta:
        name = "SGrProfilesFrameType"

    release_notes: Optional[SgrReleaseNotes] = field(
        default=None,
        metadata={
            "name": "releaseNotes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    functional_profile: Optional[SgrProfileDescriptionType] = field(
        default=None,
        metadata={
            "name": "functionalProfile",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_list_element: List[SgrDataPointsFrameType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrDeviceDescriptionType:
    """
    Device Description Geraet.
    """
    class Meta:
        name = "SGrDeviceDescriptionType"

    device_profile: Optional[SgrDeviceProfileType] = field(
        default=None,
        metadata={
            "name": "deviceProfile",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    fp_list_element: List[SgrProfilesFrameType] = field(
        default_factory=list,
        metadata={
            "name": "fpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
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
class SgrFunctionalProfileDescriptionType(SgrProfilesFrameType):
    """
    RPT Root Point for stand alone generic Functional Profile description.
    """
    class Meta:
        name = "SGrFunctionalProfileDescriptionType"
        namespace = "http://www.smartgridready.com/ns/V0/"


@dataclass
class GenDeviceFrame(SgrDeviceDescriptionType):
    """
    RPT Root Point for stand alone generic Device description.
    """
    class Meta:
        namespace = "http://www.smartgridready.com/ns/V0/"
