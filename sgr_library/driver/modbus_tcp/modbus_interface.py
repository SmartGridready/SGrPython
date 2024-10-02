# from auxiliary_functions import find_dp
import logging
from collections.abc import Mapping
from typing import Any

from aiohttp import ClientError
from pymodbus.exceptions import ConnectionException
from sgrspecification.generic import DataDirectionProduct

# from sgr_library.data_classes.ei_modbus import SgrModbusDeviceFrame
# from sgr_library.data_classes.ei_modbus.sgr_modbus_eidevice_frame import SgrModbusDataPointType
from sgrspecification.product import (
    DeviceFrame,
    ModbusDataPoint,
    ModbusFunctionalProfile,
)

from sgr_library.api import (
    ConfigurationParameter,
    DataPoint,
    DataPointProtocol,
    DeviceInformation,
    FunctionProfile,
    build_configurations_parameters,
)
from sgr_library.api.device_api import BaseSGrInterface
from sgr_library.auxiliary_functions import (
    get_address,
    get_endian,
    get_port,
    get_slave,
)
from sgr_library.validators import build_validator

from .modbus_client import SGrModbusClient

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ModBusTCPDataPoint(DataPointProtocol):
    def __init__(
        self,
        modbus_api_dp: ModbusDataPoint,
        modbus_api_fp: ModbusFunctionalProfile,
        interface: "SgrModbusInterface",
    ):
        self._dp = modbus_api_dp
        self._fp = modbus_api_fp

        self._dp_name = ""
        if self._dp.data_point and self._dp.data_point.data_point_name:
            self._dp_name = self._dp.data_point.data_point_name
        self._fp_name = ""
        if (
            self._fp.functional_profile
            and self._fp.functional_profile.functional_profile_name
        ):
            self._fp_name = self._fp.functional_profile.functional_profile_name

        self._direction = DataDirectionProduct.C
        if self._dp.data_point and self._dp.data_point.data_direction:
            self._direction = self._dp.data_point.data_direction
        self._interface = interface

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


def build_modbus_tcp_data_point(
    dp: ModbusDataPoint,
    fp: ModbusFunctionalProfile,
    interface: "SgrModbusInterface",
) -> DataPoint:
    protocol = ModBusTCPDataPoint(dp, fp, interface)
    validator = build_validator(dp.data_point.data_type)
    return DataPoint(protocol, validator)


class ModBusTCPFunctionProfile(FunctionProfile):
    def __init__(
        self,
        modbus_api_fp: ModbusFunctionalProfile,
        interface: "SgrModbusInterface",
    ):
        self._fp = modbus_api_fp
        self._interface = interface
        dps = [
            build_modbus_tcp_data_point(dp, self._fp, self._interface)
            for dp in self._fp.data_point_list.data_point_list_element
        ]
        self._data_points = {dp.name(): dp for dp in dps}
        self._fp_name = ""
        if (
            self._fp.functional_profile
            and self._fp.functional_profile.functional_profile_name
        ):
            self._fp_name = self._fp.functional_profile.functional_profile_name

    def name(self) -> str:
        return self._fp_name

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SgrModbusInterface(BaseSGrInterface):
    def __init__(self, frame: DeviceFrame) -> None:
        """
        Creates a connection from xml file data.
        Parses the xml file with xsdata library.
        :param xml_file: Name of the xml file to parse
        """
        self.root = frame
        self.ip = get_address(self.root)
        self.port = get_port(self.root)
        self.client = SGrModbusClient(self.ip, self.port)
        self.slave_id = get_slave(self.root)
        self.byte_order = get_endian(self.root)
        self._configuration_params = build_configurations_parameters(
            frame.configuration_list
        )
        # A dictionary where we cash the value of the datapoint. With name, value, timestamp and alive_time? ;)
        self.cash_dict = {}
        fps = [
            ModBusTCPFunctionProfile(profile, self)
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
        self._configuration_parameters = build_configurations_parameters(
            frame.configuration_list
        )

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configuration_parameters

    def is_connected(self) -> bool:
        return True

    async def disconnect_async(self):
        print("not implemented")

    async def connect_async(self):
        try:
            await self.client._client.connect()
            logger.info("Connected successfully.")
        except ConnectionException as e:
            logger.error(f"ConnectionException: Failed to connect: {e}")
        except TimeoutError as e:
            logger.error(f"TimeoutError: Connection timed out: {e}")
        except Exception as e:
            logger.exception(
                f"An unexpected error occurred during the connection: {e}"
            )

    def get_function_profiles(self) -> Mapping[str, FunctionProfile]:
        return self._function_profiles

    def device_information(self) -> DeviceInformation:
        return self._device_information

    async def getval(
        self, address: int, size: int, data_type: str, reg_type: str
    ) -> float:
        slave_id = self.slave_id
        order = self.byte_order
        answer = await self.client.value_decoder(
            address, size, data_type, reg_type, slave_id, order
        )
        if answer is None:
            raise ValueError("invalid read value")
        return answer

    async def setval(self, address: int, data_type: str, value: float) -> None:
        try:
            slave_id = self.slave_id
            order = self.byte_order
            await self.client.value_encoder(
                address, value, data_type, slave_id, order
            )
        except ClientError as e:
            logger.exception(f"ClientError: Failed to set value {e}")
        except ValueError as e:
            logger.error(f"ValueError: Invalid value or datatype {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
