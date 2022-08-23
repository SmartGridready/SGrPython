from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from sgr_library.data_classes.ei_modbus.sgr_modbus_eidata_types import (
    TEnumConversionFct,
    TEnumExceptionCodeType,
    TPIpmodbus,
    TPRtumodbus,
    TSgrModbusRegisterRef,
)
from sgr_library.data_classes.generic.sgr_gen_type_definitions import SgrBasicGenDataPointTypeType

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class ModbusFunctionCodesSupported:
    class Meta:
        namespace = "http://www.smartgridready.com/ns/V0/"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


class ModbusInterfaceSelectionType(Enum):
    RTU = "RTU"
    TCP_IP = "TCP/IP"
    UDP_IP = "UDP/IP"
    RTU_ASCII = "RTU-ASCII"
    TCP_IP_ASCII = "TCP/IP-ASCII"
    UDP_IP_ASCII = "UDP/IP-ASCII"


class MasterFunctionsSupportedType(Enum):
    """
    the selection of the supported Master access functions.

    :cvar PRIMITIVES: "Primitives" support ReadDiscreteInputs (code: 2)
        ReadCoils (code: 1) WriteSingleCoil (code: 5) ReadInputRegisters
        (code:4) WriteSingleHoldingRegister (code:6) for single Register
        access if dpSizeNrRegisters &gt; 1 "Primitives" supports
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
    READ_WRITE_MULTIPLE_REGISTERS = "Read/WriteMultipleRegisters"
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
class SgrAccessProtectionEnabledType:
    """Modbus datapoints may be protected by execptions.

    If this is the case, a datapoint may be selected as true with a
    range of supported exceptions. A NOT listed exception means no XY
    exception
    """
    class Meta:
        name = "SGrAccessProtectionEnabledType"

    modbus_exception: List[TEnumExceptionCodeType] = field(
        default_factory=list,
        metadata={
            "name": "modbusException",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    is_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isEnabled",
            "type": "Attribute",
        }
    )


@dataclass
class SgrModbusDataPointDescriptionType:
    """
    :ivar modbus_data_type:
    :ivar modbus_first_register_reference:
    :ivar dp_size_nr_registers:
    :ivar bitmask: Hexadecimal bitmask for mask to elmininate non used
        bit frames
    :ivar master_functions_supported: Available function/command codes
        for Master / Clients The various reading, writing and other
        operations are categorized as follows. The most "primitive"
        reads and writes are A number of sources use alternative
        terminology, for example Force Single Coil where the standard
        uses Write Single Coil.[11] Prominent entities within a Modbus
        slave are: ReadDiscreteInputs (code: 2) ReadCoils (code: 1)
        WriteSingleCoil (code: 5) WriteMultipleCoils (code:15)
        ReadInputRegisters (code:4) ReadMultipleHoldingRegisters
        (code:3) WriteSingleHoldingRegister (code:6)
        WriteMultipleHoldingRegisters (code:16) the enum "Primitives"
        means, that the current register Type supports Single
        Trasnactions If dpSizeNrRegistarts is &gt;1, also the multiple
        access functions must be supported
    :ivar modbus_jmespath:
    """
    class Meta:
        name = "SGrModbusDataPointDescriptionType"

    modbus_data_type: Optional[SgrBasicGenDataPointTypeType] = field(
        default=None,
        metadata={
            "name": "modbusDataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    modbus_first_register_reference: Optional[TSgrModbusRegisterRef] = field(
        default=None,
        metadata={
            "name": "modbusFirstRegisterReference",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    dp_size_nr_registers: Optional[int] = field(
        default=None,
        metadata={
            "name": "dpSizeNrRegisters",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    bitmask: Optional[bytes] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "format": "base16",
        }
    )
    master_functions_supported: List[MasterFunctionsSupportedType] = field(
        default_factory=list,
        metadata={
            "name": "masterFunctionsSupported",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    modbus_jmespath: Optional[str] = field(
        default=None,
        metadata={
            "name": "modbusJMESPath",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrModbusInterfaceDescriptionType:
    class Meta:
        name = "SGrModbusInterfaceDescriptionType"

    modbus_interface_selection: Optional[ModbusInterfaceSelectionType] = field(
        default=None,
        metadata={
            "name": "modbusInterfaceSelection",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    trsp_srv_modbus_tcpout_of_box: Optional[TPIpmodbus] = field(
        default=None,
        metadata={
            "name": "trspSrvModbusTCPoutOfBox",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    trsp_srv_modbus_rtuout_of_box: Optional[TPRtumodbus] = field(
        default=None,
        metadata={
            "name": "trspSrvModbusRTUoutOfBox",
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
    conversion_scheme: List[TEnumConversionFct] = field(
        default_factory=list,
        metadata={
            "name": "conversionScheme",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrModbusDataPointDescription(SgrModbusDataPointDescriptionType):
    class Meta:
        name = "SGr_ModbusDataPointDescription"
        namespace = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrModbusInterfaceDescription(SgrModbusInterfaceDescriptionType):
    class Meta:
        name = "SGr_ModbusInterfaceDescription"
        namespace = "http://www.smartgridready.com/ns/V0/"
