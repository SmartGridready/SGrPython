from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.communicator.communicator_types import CommunicatorBase
from sgrspecification.generic.base_types import GenericAttributeListFunctionalProfile
from sgrspecification.generic.data_point import DataPointBase
from sgrspecification.generic.functional_profile import FunctionalProfileDescription

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class CommunicatorFunctionalProfile(FunctionalProfileDescription):
    """
    Extends the base functional profile type with generic data points.
    """
    generic_attribute_list: Optional[GenericAttributeListFunctionalProfile] = field(
        default=None,
        metadata={
            "name": "genericAttributeList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
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
class CommunicatorFrame1(CommunicatorBase):
    """
    Data type definition for a Communicator Description.
    """
    class Meta:
        name = "CommunicatorFrame"

    functional_profile_list_element: List[CommunicatorFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "functionalProfileListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class CommunicatorFrame(CommunicatorFrame1):
    """
    RPT Root Point for Communicator.
    """
    class Meta:
        name = "communicatorFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"
