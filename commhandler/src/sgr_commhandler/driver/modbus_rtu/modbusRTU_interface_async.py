import logging
import os
from collections.abc import Mapping
from typing import Any

from pymodbus.constants import Endian
from sgr_specification.v0.generic import DataDirectionProduct, Parity

# from sgr_commhandler.data_classes.ei_modbus import SgrModbusDeviceDescriptionType
from sgr_specification.v0.product import (
    DeviceFrame,
    ModbusDataPoint,
    ModbusFunctionalProfile,
)

from sgr_commhandler.api import (
    BaseSGrInterface,
    ConfigurationParameter,
    DataPoint,
    DataPointProtocol,
    DeviceInformation,
    FunctionProfile,
    build_configurations_parameters,
)
from sgr_commhandler.driver.modbus_rtu.modbusRTU_client_async import (
    SGrModbusRTUClient,
)
from sgr_commhandler.validators import build_validator


def get_slave(root) -> int:
    """
    returns the selected slave address
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.slave_addr


def get_endian(root) -> Endian:
    return Endian.BIG


def get_baudrate(root) -> int:
    """
    returns the selected baudrate. Implemented for Even
    """
    return root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.baud_rate_selected.value


def get_parity(root) -> str:
    """
    returns the parity. Implemented for Even
    """
    parity = root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.parity_selected
    match parity:
        case Parity.EVEN:
            return "E"
        case _:
            raise NotImplementedError


def build_modbus_rtu_data_point(
    data_point: ModbusDataPoint,
    function_profile: ModbusFunctionalProfile,
    interface: "SgrModbusRtuInterface",
) -> DataPoint:
    protocol = ModBusRTUDataPoint(data_point, function_profile, interface)
    validator = build_validator(data_point.data_point.data_type)
    return DataPoint(protocol, validator)


class ModBusRTUDataPoint(DataPointProtocol):
    def __init__(
        self,
        modbus_api_dp: ModbusDataPoint,
        modbus_api_fp: ModbusFunctionalProfile,
        interface: "SgrModbusRtuInterface",
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
        return await self._interface.setval(
            self._address, self._data_type, data
        )

    async def get_val(self) -> Any:
        return await self._interface.getval(
            self._address, self._size, self._data_type, self._register_type
        )

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    def direction(self) -> DataDirectionProduct:
        return self._direction


class ModBusRTUFunctionProfile(FunctionProfile):
    def __init__(
        self,
        modbus_api_fp: ModbusFunctionalProfile,
        interface: "SgrModbusRtuInterface",
    ):
        self._fp = modbus_api_fp
        self._interface = interface
        dps = [
            build_modbus_rtu_data_point(dp, self._fp, self._interface)
            for dp in self._fp.data_point_list.data_point_list_element
        ]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp.functional_profile.functional_profile_name

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SgrModbusRtuInterface(BaseSGrInterface):
    # a global Modbus client
    globalModbusRTUClient = None

    def __init__(self, frame: DeviceFrame) -> None:
        """
        creates a connection from xml file data.
        parses the xml file with xsdata library.
        :param xml_file: name of the xml file to parse
        """
        self.root = frame
        # self.root = parser.parse(interface_file, SgrModbusDeviceDescriptionType)
        self.port = os.getenv(
            "SGR_RTU_PORT"
        )  # get_port(self.root) #TODO überlegungen machen wo Port untergebracht wird
        self._configurations_params = build_configurations_parameters(
            frame.configuration_list
        )
        self.baudrate = get_baudrate(self.root)
        self.parity = get_parity(self.root)
        self.slave_id = get_slave(self.root)
        self.byte_order = get_endian(self.root)
        fps = [
            ModBusRTUFunctionProfile(profile, self)
            for profile in self.root.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element
        ]
        self._function_profiles = {fp.name(): fp for fp in fps}
        self._device_information = DeviceInformation(
            name=frame.device_name,
            manufacture=frame.manufacturer_name,
            software_revision=frame.device_information.software_revision,
            hardware_revision=frame.device_information.hardware_revision,
            device_category=frame.device_information.device_category,
            is_local=frame.device_information.is_local_control,
        )

    def device_information(self) -> DeviceInformation:
        return self._device_information

    def is_connected(self) -> bool:
        return True

    async def connect_async(self):
        print("todo implement conenct")

    async def disconnect_async(self):
        print("todo impleemnt")

    def get_pymodbus_client(self):
        """
        returns the pymodbus client object
        """
        return self.client.client

    async def getval(
        self, address: int, size: int, data_type: str, reg_type: str
    ) -> float:
        slave_id = self.slave_id
        order = self.byte_order

        logging.debug(
            f"getVal() with address: {address}, size: {size}, data_type:{data_type}, slave_id: {slave_id}, order: {order}"
        )  # for debugging
        return await self.client.value_decoder(
            address, size, data_type, reg_type, slave_id, order
        )

    async def setval(self, address: int, data_type: str, value: float) -> None:
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

    async def async_connect(self):
        # check if there already exists a ModbusRTUClient for the communication over ModbusRTU
        if SgrModbusRtuInterface.globalModbusRTUClient is None:
            self.client = SGrModbusRTUClient(
                str(self.port), str(self.parity), int(self.baudrate)
            )
            SgrModbusRtuInterface.globalModbusRTUClient = self.client
        else:
            self.client = SgrModbusRtuInterface.globalModbusRTUClient

        if self.client:
            connected = await self.client.connect()
            if connected:
                print("Connected to ModbusRTU on Port: " + self.port)

    def get_function_profiles(self) -> Mapping[str, FunctionProfile]:
        return self._function_profiles

    def set_slave_id(self, slave_id: int):
        """
        changes the slave id for the instance
        """
        self.slave_id = slave_id
