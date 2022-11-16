from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.generic.sgr_base_device_frame import (
    SgrDataPointBaseType,
    SgrDeviceBaseType,
    SgrFunctionalProfileBaseType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class ContactApiInterfaceDescType:
    class Meta:
        name = "ContactAPI_InterfaceDescType"

    num_contacts: Optional[int] = field(
        default=None,
        metadata={
            "name": "numContacts",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    contact_stabilisation_time_ms: Optional[int] = field(
        default=None,
        metadata={
            "name": "contactStabilisationTimeMs",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class SgrContactApifunctionalProfileType(SgrFunctionalProfileBaseType):
    """
    Extends the base functional profile type with Contact API data points.
    """
    class Meta:
        name = "SGrContactAPIFunctionalProfileType"

    dp_list_element: List[SgrDataPointBaseType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrContactApideviceFrame(SgrDeviceBaseType):
    """
    RPT Root Point for Contact API Device External Interface.
    """
    class Meta:
        name = "SGrContactAPIDeviceFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"

    contact_api_interface_desc: Optional[ContactApiInterfaceDescType] = field(
        default=None,
        metadata={
            "name": "contactApiInterfaceDesc",
            "type": "Element",
            "required": True,
        }
    )
    fp_list_element: List[SgrContactApifunctionalProfileType] = field(
        default_factory=list,
        metadata={
            "name": "fpListElement",
            "type": "Element",
            "min_occurs": 1,
        }
    )
