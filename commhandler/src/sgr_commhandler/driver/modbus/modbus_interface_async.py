import logging
import random
import string
from typing import Any, Optional

from sgr_specification.v0.generic import DataDirectionProduct, Parity
from sgr_specification.v0.generic.base_types import DataTypeProduct
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

from sgr_commhandler.api import (
    DataPoint,
    DataPointProtocol,
    FunctionalProfile,
    SGrBaseInterface,
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
    match parity:
        case Parity.NONE:
            return 'N'
        case Parity.EVEN:
            return 'E'
        case Parity.ODD:
            return 'O'
        case _:
            raise NotImplementedError


def build_modbus_data_point(
    data_point: ModbusDataPointSpec,
    function_profile: ModbusFunctionalProfileSpec,
    interface: 'SGrModbusInterface',
) -> DataPoint:
    protocol = ModbusDataPoint(data_point, function_profile, interface)
    validator = build_validator(
        data_point.data_point.data_type if data_point.data_point else None
    )
    return DataPoint(protocol, validator)


def is_integer_type(data_type: DataTypeProduct | ModbusDataType) -> bool:
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


def is_float_type(data_type: DataTypeProduct | ModbusDataType) -> bool:
    return data_type.float32 is not None or data_type.float64 is not None


class ModbusDataPoint(DataPointProtocol):
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

        self._direction: DataDirectionProduct = DataDirectionProduct.C
        if self._dp_spec.data_point and self._dp_spec.data_point.data_direction:
            self._direction = self._dp_spec.data_point.data_direction

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

        self._data_type: Optional[ModbusDataType] = None
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.modbus_data_type
        ):
            self._data_type = (
                self._dp_spec.modbus_data_point_configuration.modbus_data_type
            )

        self._size = -1
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.number_of_registers
        ):
            self._size = self._dp_spec.modbus_data_point_configuration.number_of_registers

        self._register_type: RegisterType = None
        if (
            self._dp_spec.modbus_data_point_configuration
            and self._dp_spec.modbus_data_point_configuration.register_type
        ):
            self._register_type = (
                self._dp_spec.modbus_data_point_configuration.register_type
            )

    async def set_val(self, value: Any):
        # convert to device units
        if (
            self._dp_spec.data_point.unit_conversion_multiplicator
            and self._dp_spec.data_point.unit_conversion_multiplicator != 1.0
        ):
            value = (
                float(value)
                / self._dp_spec.data_point.unit_conversion_multiplicator
            )

        # round to int if modbus type is int and DP type is not
        if is_float_type(
            self._dp_spec.data_point.data_type
        ) and not is_integer_type(
            self._dp_spec.modbus_data_point_configuration.modbus_data_type
        ):
            value = value_util.round_to_int(float(value))

        return await self._interface.write_data(
            self._register_type, self._address, self._data_type, value
        )

    async def get_val(self, skip_cache: bool = False) -> Any:
        # TODO implement skip_cache
        ret_value = await self._interface.read_data(
            self._register_type, self._address, self._size, self._data_type
        )

        # convert to DP units
        if (
            self._dp_spec.data_point.unit_conversion_multiplicator
            and self._dp_spec.data_point.unit_conversion_multiplicator != 1.0
        ):
            ret_value = (
                float(ret_value)
                * self._dp_spec.data_point.unit_conversion_multiplicator
            )

        # round to int if DP type is int and modbus type is not
        if is_integer_type(
            self._dp_spec.data_point.data_type
        ) and not is_float_type(
            self._dp_spec.modbus_data_point_configuration.modbus_data_type
        ):
            ret_value = value_util.round_to_int(float(ret_value))

        return ret_value

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    def direction(self) -> DataDirectionProduct:
        return self._direction


class ModbusFunctionalProfile(FunctionalProfile):
    def __init__(
        self,
        fp_spec: ModbusFunctionalProfileSpec,
        interface: 'SGrModbusInterface',
    ):
        self._fp_spec = fp_spec
        self._interface = interface
        dps = [
            build_modbus_data_point(dp, self._fp_spec, self._interface)
            for dp in self._fp_spec.data_point_list.data_point_list_element
        ]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp_spec.functional_profile.functional_profile_name

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SGrModbusInterface(SGrBaseInterface):
    def __init__(
        self,
        frame: DeviceFrame,
        sharedRTU: bool = False,
    ):
        self._inititalize_device(frame)
        if (
            self.frame.interface_list is None
            or self.frame.interface_list.modbus_interface is None
            or self.frame.interface_list.modbus_interface.modbus_interface_description
            is None
        ):
            raise Exception('Modbus interface is undefined')

        if self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu:
            self.slave_id = get_rtu_slave_id(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
            self.serial_port = get_rtu_serial_port(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
            self.baudrate = get_rtu_baudrate(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
            self.parity = get_rtu_parity(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_rtu
            )
        elif self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp:
            self.slave_id = get_tcp_slave_id(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp
            )
            self.ip_address = get_tcp_address(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp
            )
            self.ip_port = get_tcp_port(
                self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_tcp
            )
        else:
            raise Exception('not Modbus RTU or TCP!')

        self.byte_order = get_endian(
            self.frame.interface_list.modbus_interface.modbus_interface_description
        )

        # build functional profiles
        fps = [
            ModbusFunctionalProfile(fp, self)
            for fp in self.frame.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element
        ]
        self.function_profiles = {fp.name(): fp for fp in fps}

        # unique string used in combination with shared Modbus client
        self._device_id = ''.join(random.choices(string.ascii_letters, k=8))
        self._client_wrapper: ModbusClientWrapper = None
        if (
            self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection
            == ModbusInterfaceSelection.TCPIP
        ):
            self._client_wrapper = ModbusClientWrapper(
                '',
                SGrModbusTCPClient(
                    self.ip_address, self.ip_port, self.byte_order
                ),
                shared=False,
            )
        elif (
            self.frame.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection
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
                        self.byte_order,
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
        await self._client_wrapper.connect(self._device_id)

    async def disconnect_async(self):
        await self._client_wrapper.disconnect(self._device_id)

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
