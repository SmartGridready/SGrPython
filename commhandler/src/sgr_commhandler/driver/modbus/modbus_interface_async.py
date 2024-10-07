import configparser
from collections.abc import Mapping
from typing import Any

from pymodbus.constants import Endian
from sgr_specification.v0.generic import DataDirectionProduct, Parity

from sgr_specification.v0.product import (
    DeviceFrame,
    ModbusDataPoint as ModbusDataPointSpec,
    ModbusFunctionalProfile as ModbusFunctionalProfileSpec
)

from sgr_commhandler.api import (
    BaseSGrInterface,
    ConfigurationParameter,
    DataPoint,
    DataPointProtocol,
    DeviceInformation,
    FunctionProfile,
)
from sgr_commhandler.driver.modbus.modbus_client_async import (
    SGrModbusClient, SGrModbusRTUClient, SGrModbusTCPClient
)
from sgr_commhandler.validators import build_validator
from sgr_specification.v0.product.modbus_types import ModbusInterfaceSelection


def get_rtu_slave_id(root) -> int:
    """
    returns the selected slave address
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.slave_addr


def get_tcp_slave_id(root) -> int:
    """
    returns the selected slave address
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.slave_id


def get_endian(root) -> Endian:
    return Endian.BIG


def get_tcp_address(root) -> str:
    """
    returns the selected ip address.
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.address


def get_tcp_port(root) -> int:
    """
    returns the selected ip port.
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.port


def get_rtu_serial_port(root) -> str:
    """
    returns the selected serial port.
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.port_name


def get_rtu_baudrate(root) -> int:
    """
    returns the selected baudrate.
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.baud_rate_selected


def get_rtu_parity(root) -> str:
    """
    returns the parity.
    """
    parity = root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.parity_selected
    match parity:
        case Parity.NONE:
            return "N"
        case Parity.EVEN:
            return "E"
        case Parity.ODD:
            return "O"
        case _:
            raise NotImplementedError


def build_modbus_data_point(
    data_point: ModbusDataPointSpec,
    function_profile: ModbusFunctionalProfileSpec,
    interface: "SgrModbusInterface",
) -> DataPoint:
    protocol = ModbusDataPoint(data_point, function_profile, interface)
    validator = build_validator(data_point.data_point.data_type)
    return DataPoint(protocol, validator)


class ModbusDataPoint(DataPointProtocol):
    def __init__(
        self,
        modbus_api_dp: ModbusDataPointSpec,
        modbus_api_fp: ModbusFunctionalProfileSpec,
        interface: "SgrModbusInterface",
    ):
        self._dp = modbus_api_dp
        self._fp = modbus_api_fp
        self._interface = interface

        self._dp_name = ""
        if self._dp.data_point and self._dp.data_point.data_point_name:
            self._dp_name = self._dp.data_point.data_point_name

        self._direction = DataDirectionProduct.C
        if self._dp.data_point and self._dp.data_point.data_direction:
            self._direction = self._dp.data_point.data_direction
        self._fp_name = ""
        if (
            self._fp.functional_profile
            and self._fp.functional_profile.functional_profile_name
        ):
            self._fp_name = self._fp.functional_profile.functional_profile_name
        self._address = -1
        if (
            self._dp.modbus_data_point_configuration
            and self._dp.modbus_data_point_configuration.address
        ):
            self._address = self._dp.modbus_data_point_configuration.address

        self._data_type = ""
        if (
            self._dp.modbus_data_point_configuration
            and self._dp.modbus_data_point_configuration.modbus_data_type
        ):
            for (
                key,
                value,
            ) in self._dp.modbus_data_point_configuration.modbus_data_type.__dict__.items():
                if value:
                    self._data_type = key

        self._size = -1
        if (
            self._dp.modbus_data_point_configuration
            and self._dp.modbus_data_point_configuration.number_of_registers
        ):
            self._size = (
                self._dp.modbus_data_point_configuration.number_of_registers
            )

        self._register_type = ""
        if (
            self._dp.modbus_data_point_configuration
            and self._dp.modbus_data_point_configuration.register_type
        ):
            self._register_type = (
                self._dp.modbus_data_point_configuration.register_type.value
            )

    async def set_val(self, data: Any):
        return await self._interface.set_register_value(
            self._address, self._data_type, data
        )

    async def get_val(self) -> Any:
        return await self._interface.get_register_value(
            self._address, self._size, self._data_type, self._register_type
        )

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    def direction(self) -> DataDirectionProduct:
        return self._direction


class ModbusFunctionProfile(FunctionProfile):
    def __init__(
        self,
        modbus_api_fp: ModbusFunctionalProfileSpec,
        interface: "SgrModbusInterface",
    ):
        self._fp = modbus_api_fp
        self._interface = interface
        dps = [
            build_modbus_data_point(dp, self._fp, self._interface)
            for dp in self._fp.data_point_list.data_point_list_element
        ]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp.functional_profile.functional_profile_name

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SgrModbusInterface(BaseSGrInterface):
    # a global Modbus client
    globalModbusRTUClient = None

    def __init__(self, frame: DeviceFrame, configuration: configparser.ConfigParser):
        super().__init__(frame, configuration)

        if self.root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu:
            self.slave_id = get_rtu_slave_id(self.root)
            self.serial_port = get_rtu_serial_port(self.root)
            self.baudrate = get_rtu_baudrate(self.root)
            self.parity = get_rtu_parity(self.root)
        elif self.root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp:
            self.slave_id = get_tcp_slave_id(self.root)
            self.ip_address = get_tcp_address(self.root)
            self.ip_port = get_tcp_port(self.root)
        else:
            raise Exception('not Modbus RTU or TCP!')

        self.byte_order = get_endian(self.root)
        fps = [
            ModbusFunctionProfile(profile, self)
            for profile in self.root.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element
        ]
        self._function_profiles = {fp.name(): fp for fp in fps}

        self.client: SGrModbusClient = None
        if self.root.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection == ModbusInterfaceSelection.TCPIP:
            self.client = SGrModbusTCPClient(self.ip_address, self.ip_port)
        elif self.root.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection == ModbusInterfaceSelection.RTU:
            if SgrModbusInterface.globalModbusRTUClient is None:
                self.client = SGrModbusRTUClient(self.serial_port, self.parity, self.baudrate)
                globalModbusRTUClient = self.client
            else:
                self.client = globalModbusRTUClient
        else:
            raise Exception('Unsupported Modbus interface type')

    def device_information(self) -> DeviceInformation:
        return self._device_information

    def is_connected(self) -> bool:
        return self.client.is_connected()

    async def connect_async(self):
        self.client.connect()

    async def disconnect_async(self):
        self.client.disconnect()

    async def get_register_value(
        self, address: int, size: int, data_type: str, reg_type: str
    ) -> float:
        slave_id = self.slave_id
        order = self.byte_order
        return await self.client.value_decoder(
            address, size, data_type, reg_type, slave_id, order
        )

    async def set_register_value(self, address: int, data_type: str, value: float) -> None:
        slave_id = self.slave_id
        order = self.byte_order
        await self.client.value_encoder(
            address, value, data_type, slave_id, order
        )

    def get_device_profile(self):
        return self.root.device_profile

    def get_register_type(self, dp: ModbusDataPoint) -> str:
        """
        returns register type e.g. "holdregister"
        :param fp_name: the name of the functional profile
        :param dp_name: the name of the data point.
        :returns: the type of the register
        """
        return dp.modbus_data_point_configuration.register_type.value.__str__()

    def get_datatype(self, dp: ModbusDataPoint) -> str:
        datatype = dp.modbus_data_point_configuration.modbus_data_type.__dict__
        for key in datatype:
            if datatype[key] is not None:
                return key

    def get_bit_rank(self, dp: ModbusDataPoint):
        return dp.modbus_data_point_configuration.bit_rank

    def get_address(self, dp: ModbusDataPoint):
        return dp.modbus_data_point_configuration.address

    def get_size(self, dp: ModbusDataPoint):
        return dp.modbus_data_point_configuration.number_of_registers

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configurations_params

    def get_function_profiles(self) -> Mapping[str, FunctionProfile]:
        return self._function_profiles

    def set_slave_id(self, slave_id: int):
        """
        changes the slave id for the instance
        """
        self.slave_id = slave_id
