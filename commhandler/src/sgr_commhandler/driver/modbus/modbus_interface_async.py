import logging
import random
import string
from typing import Any, Dict, Optional

from sgr_specification.v0.generic import DataDirectionProduct, Parity
from sgr_specification.v0.generic.base_types import DataTypeProduct, Units
from sgr_specification.v0.product import (
    DeviceFrame,
)
from sgr_specification.v0.product import (
    ModbusDataPoint as ModbusDataPointSpec,
)
from sgr_specification.v0.product import (
    ModbusFunctionalProfile as ModbusFunctionalProfileSpec,
)
from sgr_specification.v0.product.modbus_types import (
    BitOrder,
    ModbusDataType,
    ModbusInterfaceDescription,
    ModbusInterfaceSelection,
    ModbusRtu,
    ModbusTcp,
    RegisterType,
)
from sgr_commhandler.api.data_point_api import (
    DataPoint,
    DataPointProtocol,
)
from sgr_commhandler.api.functional_profile_api import (
    FunctionalProfile
)
from sgr_commhandler.api.device_api import (
    SGrBaseInterface
)
from sgr_commhandler.driver.modbus.modbus_client_async import (
    SGrModbusRTUClient,
    SGrModbusTCPClient,
)
from sgr_commhandler.driver.modbus.shared_client import (
    ModbusClientWrapper,
    register_shared_client,
    unregister_shared_client,
)
from sgr_commhandler.utils import value_util
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def get_rtu_slave_id(modbus_rtu: ModbusRtu) -> int:
    """
    returns the selected slave address
    """
    if modbus_rtu.slave_addr is None:
        raise Exception('No RTU slave address configured')
    return int(modbus_rtu.slave_addr)


def get_tcp_slave_id(modbus_tcp: ModbusTcp) -> int:
    """
    returns the selected slave address
    """
    if modbus_tcp.slave_id is None:
        raise Exception('No slave id configured')
    return int(modbus_tcp.slave_id)


def get_endian(modbus: ModbusInterfaceDescription) -> BitOrder:
    """
    returns the byte order.
    """
    if modbus.bit_order:
        return modbus.bit_order
    return BitOrder.BIG_ENDIAN


def get_address_offset(modbus: ModbusInterfaceDescription) -> int:
    """
    returns the address offset.
    is 0 by default and -1 when first register address is 1.
    """
    return -1 if modbus.first_register_address_is_one is not None and modbus.first_register_address_is_one else 0


def get_tcp_address(modbus_tcp: ModbusTcp) -> str:
    """
    returns the selected ip address.
    """
    if modbus_tcp.address is None:
        raise Exception('no modbus tcp address configured')
    return modbus_tcp.address


def get_tcp_port(modbus_tcp: ModbusTcp) -> int:
    """
    returns the selected ip port.
    """
    if modbus_tcp.port is None:
        raise Exception('no modbus tcp port configured')
    return int(modbus_tcp.port)


def get_rtu_serial_port(modbus_rtu: ModbusRtu) -> str:
    """
    returns the selected serial port.
    """
    if modbus_rtu.port_name is None:
        raise Exception('no modbus rtu port name configured')
    return modbus_rtu.port_name


def get_rtu_baudrate(modbus_rtu: ModbusRtu) -> int:
    """
    returns the selected baudrate.
    """
    if modbus_rtu.baud_rate_selected is None:
        raise Exception('no modbus rtu baud_rate_selected name configured')
    return int(modbus_rtu.baud_rate_selected)


def get_rtu_parity(modbus_rtu: ModbusRtu) -> str:
    """
    returns the parity.
    """
    parity = modbus_rtu.parity_selected
    if not parity:
        return 'N'
    match parity:
        case Parity.NONE.name:
            return 'N'
        case Parity.EVEN.name:
            return 'E'
        case Parity.ODD.name:
            return 'O'
        case _:
            raise NotImplementedError


def build_modbus_data_point(
    data_point: ModbusDataPointSpec,
    functional_profile: ModbusFunctionalProfileSpec,
    interface: 'SGrModbusInterface',
) -> DataPoint:
    """
    Builds a data point of a Modbus interface.
    """

    protocol = ModbusDataPoint(data_point, functional_profile, interface)
    validator = build_validator(
        data_point.data_point.data_type if data_point.data_point else None
    )
    return DataPoint(protocol, validator)


def is_integer_type(data_type: DataTypeProduct | ModbusDataType | None) -> bool:
    """
    Checks if a data type is an integer.

    Returns
    -------
    bool
        True if integer, False otherwise
    """

    if data_type is None:
        return False
    return any(
        (
            data_type.int8 is not None,
            data_type.int8_u is not None,
            data_type.int16 is not None,
            data_type.int16_u is not None,
            data_type.int32 is not None,
            data_type.int32_u is not None,
            data_type.int64 is not None,
            data_type.int64_u is not None,
        )
    )


def is_float_type(data_type: DataTypeProduct | ModbusDataType | None) -> bool:
    """
    Checks if a data type is a floating point value.

    Returns
    -------
    bool
        True if integer, False otherwise
    """

    if data_type is None:
        return False
    return data_type.float32 is not None or data_type.float64 is not None


class ModbusDataPoint(DataPointProtocol):
    """
    Implements a data point of a Modbus interface.
    """

    def __init__(
        self,
        dp_spec: ModbusDataPointSpec,
        fp_spec: ModbusFunctionalProfileSpec,
        interface: 'SGrModbusInterface',
    ):
        self._dp_spec = dp_spec
        self._fp_spec = fp_spec
        self._interface = interface

        self._dp_name: str = ''
        if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.data_point_name
        ):
            self._dp_name = self._dp_spec.data_point.data_point_name

        self._fp_name: str = ''
        if (
            self._fp_spec.functional_profile
            and self._fp_spec.functional_profile.functional_profile_name
        ):
            self._fp_name = (
                self._fp_spec.functional_profile.functional_profile_name
            )

        self._address: int = -1
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.address
        ):
            self._address = (
                self._dp_spec.modbus_data_point_configuration.address
            )

        self._data_type: ModbusDataType
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.modbus_data_type
        ):
            self._data_type = (
                self._dp_spec.modbus_data_point_configuration.modbus_data_type
            )
        else:
            raise ValueError('Modbus data type not defined')

        self._size = 0
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.number_of_registers
        ):
            self._size = self._dp_spec.modbus_data_point_configuration.number_of_registers

        self._register_type: RegisterType
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.register_type
        ):
            self._register_type = (
                self._dp_spec.modbus_data_point_configuration.register_type
            )
        else:
            raise ValueError('Modbus register type not defined')

    async def set_val(self, value: Any):
        # convert to device units
        unit_conv_factor = self._dp_spec.data_point.unit_conversion_multiplicator if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.unit_conversion_multiplicator
        ) else 1.0

        if unit_conv_factor != 1.0:
            value = float(value)  / unit_conv_factor

        # round to int if modbus type is int and DP type is not
        if is_float_type(
            self._dp_spec.data_point.data_type
            if self._dp_spec.data_point and self._dp_spec.data_point.data_type else None
        ) and not is_integer_type(
            self._dp_spec.modbus_data_point_configuration.modbus_data_type
            if self._dp_spec.modbus_data_point_configuration and self._dp_spec.modbus_data_point_configuration.modbus_data_type else None
        ):
            value = value_util.round_to_int(float(value))

        return await self._interface.write_data(
            self._register_type, self._address, self._data_type, value
        )

    async def get_val(self, parameters: Optional[dict[str, str]] = None, skip_cache: bool = False) -> Any:
        # TODO implement skip_cache
        ret_value = await self._interface.read_data(
            self._register_type, self._address, self._size, self._data_type
        )

        # convert to DP units
        unit_conv_factor = self._dp_spec.data_point.unit_conversion_multiplicator if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.unit_conversion_multiplicator
        ) else 1.0

        if unit_conv_factor != 1.0:
            ret_value = float(ret_value) * unit_conv_factor

        # round to int if DP type is int and modbus type is not
        if is_integer_type(
            self._dp_spec.data_point.data_type
            if self._dp_spec.data_point else None
        ) and not is_float_type(
            self._dp_spec.modbus_data_point_configuration.modbus_data_type
            if self._dp_spec.modbus_data_point_configuration else None
        ):
            ret_value = value_util.round_to_int(float(ret_value))

        return ret_value

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    def direction(self) -> DataDirectionProduct:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction
    
    def unit(self) -> Units:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.unit is None
        ):
            return Units.NONE
        return self._dp_spec.data_point.unit


class ModbusFunctionalProfile(FunctionalProfile):
    """
    Implements a functional profile of a Modbus interface.
    """

    def __init__(
        self,
        fp_spec: ModbusFunctionalProfileSpec,
        interface: 'SGrModbusInterface',
    ):
        self._fp_spec = fp_spec
        self._interface = interface
        dps = [
            build_modbus_data_point(dp, self._fp_spec, self._interface)
            for dp in (
                self._fp_spec.data_point_list.data_point_list_element
                if self._fp_spec.data_point_list else []
            )
        ]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp_spec.functional_profile.functional_profile_name if (
            self._fp_spec.functional_profile
            and self._fp_spec.functional_profile.functional_profile_name
        ) else ''

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SGrModbusInterface(SGrBaseInterface):
    """
    Implements a Modbus device interface.
    """

    def __init__(
        self,
        frame: DeviceFrame,
        sharedRTU: bool = False,
    ):
        self._client_wrapper: ModbusClientWrapper = None # type: ignore
        self._initialize_device(frame)
        if (
            self.device_frame.interface_list is None
            or self.device_frame.interface_list.modbus_interface is None
            or self.device_frame.interface_list.modbus_interface.modbus_interface_description
            is None
        ):
            raise Exception('Modbus interface is undefined')

        if self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu:
            self.slave_id = get_rtu_slave_id(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
            self.serial_port = get_rtu_serial_port(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
            self.baudrate = get_rtu_baudrate(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
            self.parity = get_rtu_parity(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
        elif self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp:
            self.slave_id = get_tcp_slave_id(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp
            )
            self.ip_address = get_tcp_address(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp
            )
            self.ip_port = get_tcp_port(
                self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp
            )
        else:
            raise Exception('not Modbus RTU or TCP!')

        self.byte_order = get_endian(
            self.device_frame.interface_list.modbus_interface.modbus_interface_description
        )

        self.address_offset = get_address_offset(
            self.device_frame.interface_list.modbus_interface.modbus_interface_description
        )

        # build functional profiles
        fps = [
            ModbusFunctionalProfile(fp, self)
            for fp in (
                self.device_frame.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element
                if self.device_frame.interface_list.modbus_interface.functional_profile_list else []
            )
        ]
        self.functional_profiles = {fp.name(): fp for fp in fps}

        # unique string used in combination with shared Modbus client
        self._device_id = ''.join(random.choices(string.ascii_letters, k=8))
        if (
            self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection
            == ModbusInterfaceSelection.TCPIP
        ):
            self._client_wrapper = ModbusClientWrapper(
                '',
                SGrModbusTCPClient(
                    self.ip_address, self.ip_port, endianness=self.byte_order, addr_offset=self.address_offset
                ),
                shared=False,
            )
        elif (
            self.device_frame.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection
            == ModbusInterfaceSelection.RTU
        ):
            if sharedRTU:
                logger.debug('using shared RTU client')
                self._client_wrapper = register_shared_client(
                    self.serial_port,
                    self.parity,
                    self.baudrate,
                    device_id=self._device_id,
                )
            else:
                self._client_wrapper = ModbusClientWrapper(
                    '',
                    SGrModbusRTUClient(
                        self.serial_port,
                        self.parity,
                        self.baudrate,
                        endianness=self.byte_order,
                        addr_offset=self.address_offset
                    ),
                    shared=False,
                )
        else:
            raise Exception('Unsupported Modbus interface type')

    def __del__(self):
        if self._client_wrapper and self._client_wrapper.shared:
            unregister_shared_client(
                self.serial_port, device_id=self._device_id
            )

    def is_connected(self) -> bool:
        return self._client_wrapper.is_connected(self._device_id)

    async def connect_async(self):
        await self._client_wrapper.connect_async(self._device_id)

    async def disconnect_async(self):
        await self._client_wrapper.disconnect_async(self._device_id)

    async def read_data(
        self,
        reg_type: RegisterType,
        address: int,
        size: int,
        data_type: ModbusDataType,
    ) -> Any:
        """
        Reads data from the given Modbus address(es).
        """
        slave_id = self.slave_id
        if reg_type == RegisterType.INPUT_REGISTER:
            return await self._client_wrapper.client.read_input_registers(
                slave_id, address, size, data_type
            )
        elif reg_type == RegisterType.HOLD_REGISTER:
            return await self._client_wrapper.client.read_holding_registers(
                slave_id, address, size, data_type
            )
        elif reg_type == RegisterType.COIL:
            return await self._client_wrapper.client.read_coils(
                slave_id, address, size, data_type
            )
        elif reg_type == RegisterType.DISCRETE_INPUT:
            return await self._client_wrapper.client.read_discrete_inputs(
                slave_id, address, size, data_type
            )
        else:
            raise Exception(f'cannot read from register type {reg_type}')

    async def write_data(
        self,
        reg_type: RegisterType,
        address: int,
        data_type: ModbusDataType,
        value: Any,
    ) -> None:
        """
        Writes data to the given Modbus address(es).
        """
        slave_id = self.slave_id
        if reg_type == RegisterType.HOLD_REGISTER:
            await self._client_wrapper.client.write_holding_registers(
                slave_id, address, data_type, value
            )
        elif reg_type == RegisterType.COIL:
            await self._client_wrapper.client.write_coils(
                slave_id, address, data_type, value
            )
        else:
            raise Exception(f'cannot write to register type {reg_type}')

    def set_slave_id(self, slave_id: int):
        self.slave_id = slave_id
