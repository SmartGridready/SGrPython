from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlTime
from sgr_library.data_classes.ei_gen_serial_int.sgr_serial_int_capability import (
    EBaudRateType,
    EByteLenType,
    EParityType,
    EStopBitLenType,
)
from sgr_library.data_classes.ei_modbus.sgr_modbus_eidata_types import TPIpmodbus

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class RtudevInstanceType:
    class Meta:
        name = "RTUDevInstanceType"

    device_inst_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceInstName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    slave_addr: Optional[int] = field(
        default=None,
        metadata={
            "name": "slaveAddr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TcptrspSrvInstanceType:
    class Meta:
        name = "TCPtrspSrvInstanceType"


@dataclass
class NetworkConnectionStateType:
    """This status shows, if a device is connected or not and when next
    connection attemption should be done.

    Adressing a PV Inverter e.g., this may be at the next sunrise.
    """
    class Meta:
        name = "networkConnectionStateType"

    is_connected: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isConnected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    next_attempt: Optional[XmlTime] = field(
        default=None,
        metadata={
            "name": "nextAttempt",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class RtutrspSrvInstanceType:
    class Meta:
        name = "RTUtrspSrvInstanceType"

    baud_rate: Optional[EBaudRateType] = field(
        default=None,
        metadata={
            "name": "baudRate",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    byte_len: Optional[EByteLenType] = field(
        default=None,
        metadata={
            "name": "byteLen",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    parity: Optional[EParityType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    stop_bit_len: Optional[EStopBitLenType] = field(
        default=None,
        metadata={
            "name": "stopBitLen",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TcpdevInstanceType:
    class Meta:
        name = "TCPDevInstanceType"

    dev_inst_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "devInstName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    dev_addr: Optional[TPIpmodbus] = field(
        default=None,
        metadata={
            "name": "devAddr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class NetConnectionState(NetworkConnectionStateType):
    class Meta:
        name = "netConnectionState"
        namespace = "http://www.smartgridready.com/ns/V0/"


@dataclass
class Rtutype:
    class Meta:
        name = "RTUType"

    rtu_trsp_srv_instance: Optional[RtutrspSrvInstanceType] = field(
        default=None,
        metadata={
            "name": "rtuTrspSrvInstance",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rtu_dev_instance: List[RtudevInstanceType] = field(
        default_factory=list,
        metadata={
            "name": "rtuDevInstance",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class Tcptype:
    class Meta:
        name = "TCPType"

    tcp_trsp_srv_instance: Optional[TcptrspSrvInstanceType] = field(
        default=None,
        metadata={
            "name": "tcpTrspSrvInstance",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    tcp_dev_instance: List[TcpdevInstanceType] = field(
        default_factory=list,
        metadata={
            "name": "tcpDevInstance",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class TrspServiceModbusType:
    rtu: Optional[Rtutype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    tcp: Optional[Tcptype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TrspServiceModbus(TrspServiceModbusType):
    class Meta:
        namespace = "http://www.smartgridready.com/ns/V0/"
