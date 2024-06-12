from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.data_point import DataPointBase
from sgrspecification.generic.functional_profile import FunctionalProfileBase

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class GenericDataPointList:
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
class GenericFunctionalProfile(FunctionalProfileBase):
    data_point_list: Optional[GenericDataPointList] = field(
        default=None,
        metadata={
            "name": "dataPointList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class GenericFunctionalProfileList:
    """
    List of functional profiles.
    """
    functional_profile_list_element: List[GenericFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "functionalProfileListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class GenericInterface:
    """
    Container for a device without supported transport service.
    """
    functional_profile_list: Optional[GenericFunctionalProfileList] = field(
        default=None,
        metadata={
            "name": "functionalProfileList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
