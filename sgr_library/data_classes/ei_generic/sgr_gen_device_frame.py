from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.generic.sgr_base_device_frame import (
    SgrDataPointBaseType,
    SgrDeviceBaseType,
    SgrFunctionalProfileBaseType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrGenFunctionalProfileType(SgrFunctionalProfileBaseType):
    """
    Extends the base functional profile type with generic data points.
    """
    class Meta:
        name = "SGrGenFunctionalProfileType"

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
class SgrGenDeviceFrame(SgrDeviceBaseType):
    """
    RPT Root Point for Generic Device External Interface.
    """
    class Meta:
        name = "SGrGenDeviceFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"

    fp_list_element: Optional[SgrGenFunctionalProfileType] = field(
        default=None,
        metadata={
            "name": "fpListElement",
            "type": "Element",
            "required": True,
        }
    )
