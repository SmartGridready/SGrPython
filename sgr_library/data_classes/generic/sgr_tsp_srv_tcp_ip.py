from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class TPipV4GenAddrType:
    """
    generic IPV4 device address.
    """
    class Meta:
        name = "tPipV4genAddrType"

    ip_v4port_nr: Optional[int] = field(
        default=None,
        metadata={
            "name": "ipV4portNr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    ip_v4n1: Optional[int] = field(
        default=None,
        metadata={
            "name": "ipV4n1",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 255,
        }
    )
    ip_v4n2: Optional[int] = field(
        default=None,
        metadata={
            "name": "ipV4n2",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 255,
        }
    )
    ip_v4n3: Optional[int] = field(
        default=None,
        metadata={
            "name": "ipV4n3",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 255,
        }
    )
    ip_v4n4: Optional[int] = field(
        default=None,
        metadata={
            "name": "ipV4n4",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 255,
        }
    )


@dataclass
class TPipV6GenAddrType:
    """
    generic IPV6 device address, prelimnary, untested.
    """
    class Meta:
        name = "tPipV6genAddrType"

    prelim_string_def: Optional[str] = field(
        default=None,
        metadata={
            "name": "prelimStringDef",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
