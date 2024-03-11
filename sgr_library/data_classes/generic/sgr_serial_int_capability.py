from dataclasses import dataclass, field
from enum import Enum
from typing import List

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class BaudRate(Enum):
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


class ByteLength(Enum):
    VALUE_7 = "7"
    VALUE_8 = "8"


class Parity(Enum):
    EVEN = "EVEN"
    ODD = "ODD"
    NONE = "NONE"


class StopBitLength(Enum):
    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_1_5 = "1.5"
    VALUE_2 = "2"


@dataclass
class SerialInterfaceCapability:
    baud_rates_supported: List[BaudRate] = field(
        default_factory=list,
        metadata={
            "name": "baudRatesSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    byte_len_supported: List[ByteLength] = field(
        default_factory=list,
        metadata={
            "name": "byteLenSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    parity_supported: List[Parity] = field(
        default_factory=list,
        metadata={
            "name": "paritySupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    stop_bit_len_supported: List[StopBitLength] = field(
        default_factory=list,
        metadata={
            "name": "stopBitLenSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
