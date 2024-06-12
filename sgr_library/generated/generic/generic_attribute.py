from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.base_types import (
    DataTypeFunctionalProfile,
    LegibleDescription,
    Units,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class GenericAttributeListElement:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    data_type: Optional[DataTypeFunctionalProfile] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    unit: Optional[Units] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class GenericAttributeList:
    generic_attribute_list_element: List[GenericAttributeListElement] = field(
        default_factory=list,
        metadata={
            "name": "genericAttributeListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class GenericAttributeFrame:
    """
    Generic Attribute.
    """
    class Meta:
        namespace = "http://www.smartgridready.com/ns/V0/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    generic_attribute_list: Optional[GenericAttributeList] = field(
        default=None,
        metadata={
            "name": "genericAttributeList",
            "type": "Element",
        }
    )
    data_type: Optional[DataTypeFunctionalProfile] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
        }
    )
    unit: Optional[Units] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    legible_description: List[LegibleDescription] = field(
        default_factory=list,
        metadata={
            "name": "legibleDescription",
            "type": "Element",
            "max_occurs": 4,
        }
    )
