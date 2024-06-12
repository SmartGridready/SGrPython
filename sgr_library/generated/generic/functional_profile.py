from dataclasses import dataclass, field
from typing import List, Optional
from sgrspecification.generic.base_types import (
    AlternativeNames,
    FunctionalProfileIdentification,
    GenericAttributeListProduct,
    LegibleDescription,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class FunctionalProfileDescription:
    """
    Functional profile properties.

    :ivar functional_profile_name:
    :ivar functional_profile_identification:
    :ivar alternative_names:
    :ivar legible_description: Published and printable information
        related to this functional profile
    :ivar programmer_hints: additional device-specific implementation
        hints for this functional profile
    """
    functional_profile_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "functionalProfileName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    functional_profile_identification: Optional[FunctionalProfileIdentification] = field(
        default=None,
        metadata={
            "name": "functionalProfileIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    alternative_names: Optional[AlternativeNames] = field(
        default=None,
        metadata={
            "name": "alternativeNames",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    legible_description: List[LegibleDescription] = field(
        default_factory=list,
        metadata={
            "name": "legibleDescription",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    programmer_hints: List[LegibleDescription] = field(
        default_factory=list,
        metadata={
            "name": "programmerHints",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )


@dataclass
class FunctionalProfileBase:
    """
    Functional profile element.
    """
    functional_profile: Optional[FunctionalProfileDescription] = field(
        default=None,
        metadata={
            "name": "functionalProfile",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    generic_attribute_list: Optional[GenericAttributeListProduct] = field(
        default=None,
        metadata={
            "name": "genericAttributeList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
