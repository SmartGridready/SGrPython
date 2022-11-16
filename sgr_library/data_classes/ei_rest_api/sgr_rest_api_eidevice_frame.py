from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.ei_rest_api.sgr_rest_api_eidata_types import (
    SgrAttr4RestApitype,
    SgrRestApidataPointDescriptionType,
    SgrRestApiinterfaceDescriptionType,
)
from data_classes.generic.sgr_base_device_frame import (
    SgrDataPointBaseType,
    SgrDeviceBaseType,
    SgrFunctionalProfileBaseType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrRestApidataPointType(SgrDataPointBaseType):
    """
    Extends the base data point type with Rest API attributes and data points.
    """
    class Meta:
        name = "SGrRestAPIDataPointType"

    rest_apidata_point: List[SgrRestApidataPointDescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "restAPIDataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    rest_apiattr: List[SgrAttr4RestApitype] = field(
        default_factory=list,
        metadata={
            "name": "restAPIAttr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrRestApifunctionalProfileType(SgrFunctionalProfileBaseType):
    """
    Extends the base functional profile type with Rest API attributes and data
    points.
    """
    class Meta:
        name = "SGrRestAPIFunctionalProfileType"

    rest_apiattr: List[SgrAttr4RestApitype] = field(
        default_factory=list,
        metadata={
            "name": "restAPIAttr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_list_element: List[SgrRestApidataPointType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrRestApideviceFrame(SgrDeviceBaseType):
    """
    RPT Root Point for Rest API Device External Interface.
    """
    class Meta:
        name = "SGrRestAPIDeviceFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"

    rest_apiattr: List[SgrAttr4RestApitype] = field(
        default_factory=list,
        metadata={
            "name": "restAPIAttr",
            "type": "Element",
        }
    )
    rest_apiinterface_desc: Optional[SgrRestApiinterfaceDescriptionType] = field(
        default=None,
        metadata={
            "name": "restAPIInterfaceDesc",
            "type": "Element",
            "required": True,
        }
    )
    fp_list_element: List[SgrRestApifunctionalProfileType] = field(
        default_factory=list,
        metadata={
            "name": "fpListElement",
            "type": "Element",
            "min_occurs": 1,
        }
    )
