from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.data_point import DataPointBase
from sgrspecification.generic.functional_profile import FunctionalProfileBase

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class ContactInterfaceDescription:
    """
    Contact interface properties.

    :ivar number_of_contacts:
    :ivar contact_stabilisation_time_ms: Time in milliseconds until a
        contact has reached a stable state after switching
    """
    number_of_contacts: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfContacts",
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
class ContactsDataPointList:
    """
    List of data points.
    """
    data_point_list_element: List[DataPointBase] = field(
        default_factory=list,
        metadata={
            "name": "dataPointListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class ContactFunctionalProfile(FunctionalProfileBase):
    data_point_list: List[ContactsDataPointList] = field(
        default_factory=list,
        metadata={
            "name": "dataPointList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class ContactFunctionalProfileList:
    """
    List of functional profiles.
    """
    functional_profile_list_element: List[ContactFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "functionalProfileListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class ContactInterface:
    """
    Container for a device with contacts.
    """
    contact_interface_description: Optional[ContactInterfaceDescription] = field(
        default=None,
        metadata={
            "name": "contactInterfaceDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    functional_profile_list: Optional[ContactFunctionalProfileList] = field(
        default=None,
        metadata={
            "name": "functionalProfileList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
