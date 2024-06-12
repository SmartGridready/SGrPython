from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from sgrspecification.generic.base_types import (
    BitmapProduct,
    EmptyType,
    EnumType,
    ScalingFactor,
)
from sgrspecification.generic.sgr_serial_int_capability import (
    BaudRate,
    ByteLength,
    Parity,
    SerialInterfaceCapability,
    StopBitLength,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class BitOrder(Enum):
    """
    Modbus bit orders are used to apply different conversion transformations to
    data between Modbus device and IEC61850 devices.
    """
    BIG_ENDIAN = "BigEndian"
    CHANGE_DWORD_ORDER = "ChangeDWordOrder"
    CHANGE_WORD_ORDER = "ChangeWordOrder"
    CHANGE_BYTE_ORDER = "ChangeByteOrder"
    CHANGE_BIT_ORDER = "ChangeBitOrder"


class MasterFunctionsSupported(Enum):
    """Available function/command codes for Master / Clients The various
    reading, writing and other operations are categorized as follows.

    The most "primitive" reads and writes are A number of sources use
    alternative terminology, for example Force Single Coil where the
    standard uses Write Single Coil.[11] Prominent entities within a
    Modbus slave are: ReadDiscreteInputs (code: 2) ReadCoils (code: 1)
    WriteSingleCoil (code: 5) WriteMultipleCoils (code:15)
    ReadInputRegisters (code:4) ReadMultipleHoldingRegisters (code:3)
    WriteSingleHoldingRegister (code:6) WriteMultipleHoldingRegisters
    (code:16) the enum "Primitives" means, that the current register
    Type supports Single Trasnactions If dpSizeNrRegistarts is &gt;1,
    also the multiple access functions must be supported

    :cvar PRIMITIVES: "Primitives" support ReadDiscreteInputs (code: 2)
        ReadCoils (code: 1) WriteSingleCoil (code: 5) ReadInputRegisters
        (code:4) WriteSingleHoldingRegister (code:6) for single Register
        access if numberOfRegisters &gt; 1 "Primitives" supports
        ReadMultipleHoldingRegisters (code:3) WriteMultipleCoils
        (code:15) WriteMultipleHoldingRegisters (code:16) for the
        register Type being adressed
    :cvar READ_DISCRETE_INPUTS: Master function code= 2
    :cvar READ_COILS: Master function code: 1
    :cvar WRITE_SINGLE_COIL: Master function code: 5
    :cvar WRITE_MULTIPLE_COILS: Master function code:15
    :cvar READ_INPUT_REGISTERS: Master function code:4
    :cvar READ_MULTIPLE_HOLDING_REGISTERS: Master function code:3
    :cvar WRITE_SINGLE_HOLDING_REGISTER: Master function code:6
    :cvar WRITE_MULTIPLE_HOLDING_REGISTERS: Master function code:16
    :cvar READ_WRITE_MULTIPLE_REGISTERS: Master function code:23
    :cvar MASK_WRITE_REGISTER: Master function code:22
    :cvar READ_FIFOQUEUE: Master function code:24
    :cvar READ_FILE_RECORD: Master function code:20
    :cvar WRITE_FILE_RECORD: Master function code:21
    :cvar READ_EXCEPTION_STATUS: Master function code:7
    :cvar DIAGNOSTIC: Master function code:8
    :cvar GET_COM_EVENT_COUNTER: Master function code:11
    :cvar GET_COM_EVENT_LOG: Master function code:12
    :cvar REPORT_SLAVE_ID: Master function code:17
    :cvar READ_DEVICE_IDENTIFICATION: Master function code:43
    """
    PRIMITIVES = "Primitives"
    READ_DISCRETE_INPUTS = "ReadDiscreteInputs"
    READ_COILS = "ReadCoils"
    WRITE_SINGLE_COIL = "WriteSingleCoil"
    WRITE_MULTIPLE_COILS = "WriteMultipleCoils"
    READ_INPUT_REGISTERS = "ReadInputRegisters"
    READ_MULTIPLE_HOLDING_REGISTERS = "ReadMultipleHoldingRegisters"
    WRITE_SINGLE_HOLDING_REGISTER = "WriteSingleHoldingRegister"
    WRITE_MULTIPLE_HOLDING_REGISTERS = "WriteMultipleHoldingRegisters"
    READ_WRITE_MULTIPLE_REGISTERS = "ReadWriteMultipleRegisters"
    MASK_WRITE_REGISTER = "MaskWriteRegister"
    READ_FIFOQUEUE = "ReadFIFOQueue"
    READ_FILE_RECORD = "ReadFileRecord"
    WRITE_FILE_RECORD = "WriteFileRecord"
    READ_EXCEPTION_STATUS = "ReadExceptionStatus"
    DIAGNOSTIC = "Diagnostic"
    GET_COM_EVENT_COUNTER = "GetComEventCounter"
    GET_COM_EVENT_LOG = "GetComEventLog"
    REPORT_SLAVE_ID = "ReportSlaveID"
    READ_DEVICE_IDENTIFICATION = "ReadDeviceIdentification"


@dataclass
class ModbusBoolean:
    """
    Modbus specific boolean definition.
    """
    true_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "trueValue",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    false_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "falseValue",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


class ModbusExceptionCode(Enum):
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


class ModbusInterfaceSelection(Enum):
    """
    Type of Modbus interface.
    """
    RTU = "RTU"
    TCPIP = "TCPIP"
    UDPIP = "UDPIP"
    RTU_ASCII = "RTU-ASCII"
    TCPIP_ASCII = "TCPIP-ASCII"
    UDPIP_ASCII = "UDPIP-ASCII"


class ModbusLayer6Deviation(Enum):
    """
    this type is used to manage non standard data type definitions at ISO/OSI
    Layer 6.

    :cvar VALUE_2_REG_BASE1000_L2_H: 2 Registers show a combined value,
        as example in kWh and MWh beginning with lower range @ lower
        address
    :cvar VALUE_2_REG_BASE1000_H2_L: 2 Registers show a combined value,
        as example in kWh and MWh beginning with lower range @ higher
        address
    """
    VALUE_2_REG_BASE1000_L2_H = "2RegBase1000_L2H"
    VALUE_2_REG_BASE1000_H2_L = "2RegBase1000_H2L"


@dataclass
class ModbusTcp:
    """Modbus IP address:Specific P elements for Modbus over IP protocol.

    This definition is partially inherited from 61850-80-5's
    tPTypeModbusIPEnum typedef but reduced to a single interface (not
    redundant adresses RG1 and RG2) and information layer definitions
    """
    port: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    address: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "pattern": r"\d+\.\d+\.\d+\.\d+|\{\{.*\}\}",
        }
    )
    slave_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "slaveId",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class RegisterType(Enum):
    """Type of the Modbus Data.

    For slave-role, definition of the Object Type of the
    data: Discretes Input: Single bit, Read-Only; Coils: Single bit, Read-Write; Input
    Registers: 16-bit word, Read-Only; Holding Registers: 16-bit word, Read-Write.
    """
    COIL = "Coil"
    DISCRETE_INPUT = "DiscreteInput"
    INPUT_REGISTER = "InputRegister"
    HOLD_REGISTER = "HoldRegister"


@dataclass
class AccessProtectionEnabled:
    """Modbus datapoints may be protected by execptions.

    If this is the case, a datapoint may be selected as true with a
    range of supported exceptions. A NOT listed exception means no XY
    exception
    """
    modbus_exception_code: List[ModbusExceptionCode] = field(
        default_factory=list,
        metadata={
            "name": "modbusExceptionCode",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    is_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isEnabled",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class MasterFunctionsSupportedList:
    """Available function/command codes for Master / Clients The various
    reading, writing and other operations are categorized as follows.

    The most "primitive" reads and writes are A number of sources use
    alternative terminology, for example Force Single Coil where the
    standard uses Write Single Coil.[11] Prominent entities within a
    Modbus slave are: ReadDiscreteInputs (code: 2) ReadCoils (code: 1)
    WriteSingleCoil (code: 5) WriteMultipleCoils (code:15)
    ReadInputRegisters (code:4) ReadMultipleHoldingRegisters (code:3)
    WriteSingleHoldingRegister (code:6) WriteMultipleHoldingRegisters
    (code:16) the enum "Primitives" means, that the current register
    Type supports Single Trasnactions If dpSizeNrRegistarts is &gt;1,
    also the multiple access functions must be supported
    """
    master_functions_supported: List[MasterFunctionsSupported] = field(
        default_factory=list,
        metadata={
            "name": "masterFunctionsSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class ModbusDataType:
    """
    Modbus specific data types.
    """
    boolean: Optional[ModbusBoolean] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int8U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int16U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int32U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int64U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float32: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float64: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    date_time: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "dateTime",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    string: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    enum: Optional[EnumType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    bitmap: Optional[BitmapProduct] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ModbusRtu:
    """
    Modbus RTU serial port configuration.
    """
    slave_addr: Optional[int] = field(
        default=None,
        metadata={
            "name": "slaveAddr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    baud_rate_selected: Optional[BaudRate] = field(
        default=None,
        metadata={
            "name": "baudRateSelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    byte_len_selected: Optional[ByteLength] = field(
        default=None,
        metadata={
            "name": "byteLenSelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    parity_selected: Optional[Parity] = field(
        default=None,
        metadata={
            "name": "paritySelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    stop_bit_len_selected: Optional[StopBitLength] = field(
        default=None,
        metadata={
            "name": "stopBitLenSelected",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    serial_interface_capability: Optional[SerialInterfaceCapability] = field(
        default=None,
        metadata={
            "name": "serialInterfaceCapability",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class TimeSyncBlockNotification:
    """
    Time sync block notifications are used to describe a block of registers
    that can be feched simultaneously.

    :ivar block_cache_identification: Identification (used by data
        points for referencing)
    :ivar first_address: Start address of block
    :ivar size: Block size in number of registers
    :ivar register_type: Modbus register type
    :ivar time_to_live_ms: Block cache time in milliseconds
    """
    block_cache_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "blockCacheIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    first_address: Optional[int] = field(
        default=None,
        metadata={
            "name": "firstAddress",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    size: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    register_type: Optional[RegisterType] = field(
        default=None,
        metadata={
            "name": "registerType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    time_to_live_ms: Optional[int] = field(
        default=None,
        metadata={
            "name": "timeToLiveMs",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class ModbusAttributes:
    """
    Modbus-specific attributes.

    :ivar scaling_factor: generic value = dataPoint * m * 10^p
    :ivar step_by_increment: each didgit
    :ivar sunssf: a Sunpec specific attribute (scalefactor p -10 ...
        +10) generic value = dataPoint * 10^p note: Sunspec uses sunssf
        usually as Modbus Register with dynamic values check attribute
        "timeAlignedNotification"
    :ivar polling_latency_ms: The time for a master slave communication
        cycle in ms
    :ivar access_protection:
    :ivar layer6_deviation:
    """
    scaling_factor: Optional[ScalingFactor] = field(
        default=None,
        metadata={
            "name": "scalingFactor",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    step_by_increment: Optional[int] = field(
        default=None,
        metadata={
            "name": "stepByIncrement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sunssf: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    polling_latency_ms: Optional[int] = field(
        default=None,
        metadata={
            "name": "pollingLatencyMs",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    access_protection: Optional[AccessProtectionEnabled] = field(
        default=None,
        metadata={
            "name": "accessProtection",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    layer6_deviation: Optional[ModbusLayer6Deviation] = field(
        default=None,
        metadata={
            "name": "layer6Deviation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ModbusDataPointConfiguration:
    """
    Detailed configuration for modbus data point.

    :ivar modbus_data_type:
    :ivar address: 2-bytes-word address: could be a register address (to
        address a modbus register - inputRegister or holdRegister) or a
        part of a bit address (together with bitRank coil -
        discreteInput)
    :ivar bit_rank:
    :ivar register_type:
    :ivar number_of_registers: Number of 16-bit registers of this data
        point
    """
    modbus_data_type: Optional[ModbusDataType] = field(
        default=None,
        metadata={
            "name": "modbusDataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    address: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    bit_rank: Optional[int] = field(
        default=None,
        metadata={
            "name": "bitRank",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_inclusive": 0,
            "max_inclusive": 15,
        }
    )
    register_type: Optional[RegisterType] = field(
        default=None,
        metadata={
            "name": "registerType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    number_of_registers: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfRegisters",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class ModbusInterfaceDescription:
    """
    Modbus interface properties.

    :ivar modbus_interface_selection:
    :ivar modbus_tcp:
    :ivar modbus_rtu:
    :ivar first_register_address_is_one: True if the first register
        starts at 1
    :ivar bit_order:
    :ivar master_functions_supported_list:
    """
    modbus_interface_selection: Optional[ModbusInterfaceSelection] = field(
        default=None,
        metadata={
            "name": "modbusInterfaceSelection",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    modbus_tcp: Optional[ModbusTcp] = field(
        default=None,
        metadata={
            "name": "modbusTcp",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    modbus_rtu: Optional[ModbusRtu] = field(
        default=None,
        metadata={
            "name": "modbusRtu",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    first_register_address_is_one: Optional[bool] = field(
        default=None,
        metadata={
            "name": "firstRegisterAddressIsOne",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    bit_order: Optional[BitOrder] = field(
        default=None,
        metadata={
            "name": "bitOrder",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    master_functions_supported_list: Optional[MasterFunctionsSupportedList] = field(
        default=None,
        metadata={
            "name": "masterFunctionsSupportedList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
