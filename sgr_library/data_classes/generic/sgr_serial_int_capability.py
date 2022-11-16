from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class EBaudRateType(Enum):
    VALUE_300 = "300"
    VALUE_600 = "600"
    VALUE_1200 = "1200"
    VALUE_2400 = "2400"
    VALUE_4800 = "4800"
    VALUE_5600 = "5600"
    VALUE_9600 = "9600"
    VALUE_14400 = "14400"
    VALUE_19200 = "19200"
    VALUE_38400 = "38400"
    VALUE_57600 = "57600"
    VALUE_115200 = "115200"
    VALUE_128000 = "128000"
    VALUE_230400 = "230400"
    VALUE_256000 = "256000"


class EByteLenType(Enum):
    VALUE_7 = "7"
    VALUE_8 = "8"


class EParityType(Enum):
    EVEN = "EVEN"
    ODD = "ODD"
    NONE = "NONE"


class EStopBitLenType(Enum):
    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_1_5 = "1.5"
    VALUE_2 = "2"


@dataclass
class SgrSerialInterfaceCapabilityType:
    class Meta:
        name = "SGrSerialInterfaceCapabilityType"

    baud_rates_supported: List[EBaudRateType] = field(
        default_factory=list,
        metadata={
            "name": "baudRatesSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    byte_len_supported: List[EByteLenType] = field(
        default_factory=list,
        metadata={
            "name": "byteLenSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    parity_supported: List[EParityType] = field(
        default_factory=list,
        metadata={
            "name": "paritySupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    stop_bit_len_supported: List[EStopBitLenType] = field(
        default_factory=list,
        metadata={
            "name": "stopBitLenSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class BaudRatesSupported:
    class Meta:
        name = "baudRatesSupported"
        namespace = "http://www.smartgridready.com/ns/V0/"

    value: Optional[EBaudRateType] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class ByteLenSupported:
    class Meta:
        name = "byteLenSupported"
        namespace = "http://www.smartgridready.com/ns/V0/"

    value: Optional[EByteLenType] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class ParitySupported:
    class Meta:
        name = "paritySupported"
        namespace = "http://www.smartgridready.com/ns/V0/"

    value: Optional[EParityType] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class StopBitLenSupported:
    class Meta:
        name = "stopBitLenSupported"
        namespace = "http://www.smartgridready.com/ns/V0/"

    value: Optional[EStopBitLenType] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class SgrSerialInterfaceCapability(SgrSerialInterfaceCapabilityType):
    class Meta:
        name = "SGrSerialInterfaceCapability"
        namespace = "http://www.smartgridready.com/ns/V0/"
