from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.generic.sgr_base_device_frame import SgrDataPointBaseType
from data_classes.generic.sgr_gen_type_definitions import (
    SgrAttr4GenericType,
    SgrReleaseNotes,
)
from data_classes.generic.sgr_profile_description_type import SgrProfileDescriptionType

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrFunctionalProfileFrame:
    """
    RPT Root Point for stand alone generic Functional Profile description.
    """
    class Meta:
        name = "SGrFunctionalProfileFrame"
        namespace = "http://www.smartgridready.com/ns/V0/"

    release_notes: Optional[SgrReleaseNotes] = field(
        default=None,
        metadata={
            "name": "releaseNotes",
            "type": "Element",
        }
    )
    functional_profile: Optional[SgrProfileDescriptionType] = field(
        default=None,
        metadata={
            "name": "functionalProfile",
            "type": "Element",
            "required": True,
        }
    )
    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
        }
    )
    dp_list_element: List[SgrDataPointBaseType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "min_occurs": 1,
        }
    )
