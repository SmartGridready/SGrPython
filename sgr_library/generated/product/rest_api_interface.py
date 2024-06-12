from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.data_point import DataPointBase
from sgrspecification.generic.functional_profile import FunctionalProfileBase
from sgrspecification.product.rest_api_types import (
    RestApiDataPointConfiguration,
    RestApiInterfaceDescription,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class RestApiDataPoint(DataPointBase):
    rest_api_data_point_configuration: Optional[RestApiDataPointConfiguration] = field(
        default=None,
        metadata={
            "name": "restApiDataPointConfiguration",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class RestApiDataPointList:
    """
    List of data points.
    """
    data_point_list_element: List[RestApiDataPoint] = field(
        default_factory=list,
        metadata={
            "name": "dataPointListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class RestApiFunctionalProfile(FunctionalProfileBase):
    data_point_list: Optional[RestApiDataPointList] = field(
        default=None,
        metadata={
            "name": "dataPointList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class RestApiFunctionalProfileList:
    """
    List of functional profiles.
    """
    functional_profile_list_element: List[RestApiFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "functionalProfileListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class RestApiInterface:
    """
    Container for a rest api device.
    """
    rest_api_interface_description: Optional[RestApiInterfaceDescription] = field(
        default=None,
        metadata={
            "name": "restApiInterfaceDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    functional_profile_list: Optional[RestApiFunctionalProfileList] = field(
        default=None,
        metadata={
            "name": "functionalProfileList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
