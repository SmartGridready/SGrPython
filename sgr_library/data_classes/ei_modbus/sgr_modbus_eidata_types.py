from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from sgr_library.data_classes.ei_gen_serial_int.sgr_serial_int_capability import (
    SgrSerialInterfaceCapabilityType,
    EBaudRateType,
    EByteLenType,
    EParityType,
    EStopBitLenType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class IpAddrtype:
    """
    Modbus device address.
    """
    class Meta:
        name = "ipADDRType"

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


class TEnumConversionFct(Enum):
    """Modbus conversion functions are used to apply different transformations
    to data between Modbus device and IEC61850 devices. There are different
    kind of conversions, depending on.

    operation to apply: - Bit conversion: ChangeDWordOrder,
    ChangeWordOrder, ChangeByteOrder, ChangeBitOrder
    """
    BIG_ENDIAN = "BigEndian"
    CHANGE_DWORD_ORDER = "ChangeDWordOrder"
    CHANGE_WORD_ORDER = "ChangeWordOrder"
    CHANGE_BYTE_ORDER = "ChangeByteOrder"
    CHANGE_BIT_ORDER = "ChangeBitOrder"


class TEnumExceptionCodeType(Enum):
    """
    Type of the Modbus Exceptions sent by Slave (Server) responses.

    :cvar ILLEGAL_FUNCTION: "1: Illegal Function Function code received
        in the query is not recognized or allowed by slave"
    :cvar ILLEGAL_ADDRESS: 2: Illegal Data Address Data address of some
        or all the required entities are not allowed or do not exist in
        slave
    :cvar ILLEGAL_DATA_VALUE: 3: Illegal Data Value Value is not
        accepted by slave
    :cvar SLAVE_FAILURE: 4: Slave (Server) Device Failure Unrecoverable
        error occurred while slave was attempting to perform requested
        action
    :cvar ACK: 5: Acknowledge Slave has accepted request and is
        processing it, but a long duration of time is required. This
        response is returned to prevent a timeout error from occurring
        in the master. Master can next issue a Poll Program Complete
        message to determine whether processing is completed
    :cvar SLAVE_BUSY: 6: Slave (Server) Device Busy Slave is engaged in
        processing a long-duration command. Master should retry later
    :cvar NACK: 7: Negative Acknowledge Slave (Server) cannot perform
        the programming functions. Master should request diagnostic or
        error information from slave
    :cvar MEMORY_PARITY_ERR: 8: Memory Parity Error Slave (Server)
        detected a parity error in memory. Master can retry the request,
        but service may be required on the slave device
    :cvar GTWY_PATH_ERR: 10: Gateway Path Unavailable Specialized for
        Modbus gateways. Indicates a misconfigured gateway
    :cvar GTWY_TARGET_ERR: 11: Gateway Target Device Failed to Respond
        Specialized for Modbus gateways. Sent when slave fails to
        respond
    """
    ILLEGAL_FUNCTION = "IllegalFunction"
    ILLEGAL_ADDRESS = "IllegalAddress"
    ILLEGAL_DATA_VALUE = "IllegalDataValue"
    SLAVE_FAILURE = "SlaveFailure"
    ACK = "ACK"
    SLAVE_BUSY = "SlaveBusy"
    NACK = "NACK"
    MEMORY_PARITY_ERR = "MemoryParityErr"
    GTWY_PATH_ERR = "GtwyPathErr"
    GTWY_TARGET_ERR = "GtwyTargetErr"


class TEnumObjectType(Enum):
    """Type of the Modbus Data.

    For slave-role, definition of
    the Object Type of the data: Discretes Input: Single bit, Read-Only;
    Coils: Single bit, Read-Write; Input Registers: 16-bit word,
    Read-Only; Holding Registers: 16-bit word, Read-Write.
    """
    COIL = "Coil"
    DISCRETE_INPUT = "DiscreteInput"
    INPUT_REGISTER = "InputRegister"
    HOLD_REGISTER = "HoldRegister"


@dataclass
class TimeSyncBlockNotificationType:
    class Meta:
        name = "timeSyncBlockNotificationType"

    block_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "blockNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    timeout_ms: Optional[int] = field(
        default=None,
        metadata={
            "name": "timeoutMs",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TPIpmodbus:
    """Modbus IP address:Specific P elements for Modbus over IP protocol.

    This definition is partially inherited from 61850-80-5's
    tPTypeModbusIPEnum typedef but reduced to a single interface (not
    redundant adresses RG1 and RG2) and information layer definitions
    """
    class Meta:
        name = "tP_IPModbus"

    port: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    address: Optional[IpAddrtype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    slave_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "slaveID",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TPRtumodbus:
    class Meta:
        name = "tP_RTUModbus"

    slave_addr: Optional[int] = field(
        default=None,
        metadata={
            "name": "slaveAddr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    baud_rate_selected: Optional[EBaudRateType] = field(
        default=None,
        metadata={
            "name": "baudRateSelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    byte_len_selected: Optional[EByteLenType] = field(
        default=None,
        metadata={
            "name": "byteLenSelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    parity_selected: Optional[EParityType] = field(
        default=None,
        metadata={
            "name": "paritySelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    stop_bit_len_selected: Optional[EStopBitLenType] = field(
        default=None,
        metadata={
            "name": "stopBitLenSelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    serial_interface_capability: Optional[SgrSerialInterfaceCapabilityType] = field(
        default=None,
        metadata={
            "name": "serialInterfaceCapability",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TSgrModbusRegisterRef:
    """2-bytes-word address: could be a register address (to.

    address a modbus register - inputRegister or holdRegister) or a part
    of a bit address, see bitRank definition

    :ivar addr: 2-bytes-word address: could be a register address (to
        address a modbus register - inputRegister or holdRegister) or a
        part of a bit address, see bitRank definition
    :ivar bit_rank: The bit rank used to define a bit address
        (bitAddress = addr x 16 + bitRank)
    :ivar register_type: For slave-role, definition of the Object Type
        of the data: Discretes Input: Single bit, Read-Only; Coils:
        Single bit, Read-Write; Input Registers: 16-bit word, Read-Only;
        Holding Registers: 16-bit word, Read-Write.
    """
    class Meta:
        name = "tSGrModbus_RegisterRef"

    addr: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    bit_rank: Optional[int] = field(
        default=None,
        metadata={
            "name": "bitRank",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 15,
        }
    )
    register_type: Optional[TEnumObjectType] = field(
        default=None,
        metadata={
            "name": "registerType",
            "type": "Attribute",
            "required": True,
        }
    )
