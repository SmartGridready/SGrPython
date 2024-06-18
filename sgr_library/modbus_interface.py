from typing import Any

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
import time

from sgr_library.api import DeviceInformation, FunctionProfile, DataPointProtocol, DataPoint, ConfigurationParameter, \
    build_configurations_parameters
from sgr_library.api.device_api import BaseSGrInterface
from sgr_library.converters import build_converter
from sgrspecification.generic import DataDirectionProduct
from sgr_library.exceptions import DataPointException, FunctionalProfileException, DataProcessingError, \
    DeviceInformationError, InvalidEndianType
from pymodbus.exceptions import ConnectionException
from aiohttp import ClientError

# from sgr_library.data_classes.ei_modbus import SgrModbusDeviceFrame
# from sgr_library.data_classes.ei_modbus.sgr_modbus_eidevice_frame import SgrModbusDataPointType

from sgrspecification.product import DeviceFrame, ModbusDataPoint, ModbusFunctionalProfile
from sgr_library.auxiliary_functions import get_address, get_endian, get_port, get_slave
from sgrspecification.generic import DataDirectionProduct

from sgr_library.modbus_client import SGrModbusClient
# from auxiliary_functions import find_dp
import asyncio

import logging

from sgr_library.validators import build_validator

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ModBusTCPDataPoint(DataPointProtocol):

    def __init__(self, modbus_api_dp: ModbusDataPoint, modbus_api_fp: ModbusFunctionalProfile,
                 interface: 'SgrModbusInterface'):
        self._dp = modbus_api_dp
        self._fp = modbus_api_fp
        self._interface = interface

    async def write(self, data: Any):
        return await self._interface.setval(self.name()[0], self.name()[1], data)

    async def read(self) -> Any:
        return await self._interface.getval(self.name()[0], self.name()[1])

    def name(self) -> tuple[str, str]:
        return self._fp.functional_profile.functional_profile_name, self._dp.data_point.data_point_name

    def direction(self) -> DataDirectionProduct:
        return self._dp.data_point.data_direction


def build_modbus_tcp_data_point(dp: ModbusDataPoint, fp: ModbusFunctionalProfile,
                                interface: 'SgrModbusInterface') -> DataPoint:
    protocol = ModBusTCPDataPoint(dp, fp, interface)
    converter = build_converter(dp.data_point.unit)
    validator = build_validator(dp.data_point.data_type)
    return DataPoint(protocol, converter, validator)


class ModBusTCPFunctionProfile(FunctionProfile):

    def __init__(self, modbus_api_fp: ModbusFunctionalProfile, interface: 'SgrModbusInterface'):
        self._fp = modbus_api_fp
        self._interface = interface
        dps = [build_modbus_tcp_data_point(dp, self._fp, self._interface) for dp in
               self._fp.data_point_list.data_point_list_element]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp.functional_profile.functional_profile_name

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
        self._configuration_params = build_configurations_parameters(frame.configuration_list)
        # A dictionary where we cash the value of the datapoint. With name, value, timestamp and alive_time? ;)
        self.cash_dict = {}
        fps = [ModBusTCPFunctionProfile(profile, self) for profile in
               self.root.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element]
        self._function_profiles = {fp.name(): fp for fp in fps}
        self._device_information = DeviceInformation(
            name=frame.device_name,
            manufacture=frame.manufacturer_name,
            software_revision=frame.device_information.software_revision,
            hardware_revision=frame.device_information.hardware_revision,
            device_category=frame.device_information.device_category,
            is_local=frame.device_information.is_local_control
        )
        self._configuration_parameters = build_configurations_parameters(frame.configuration_list)

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configuration_parameters

    async def connect(self):
        try:
            await self.client.client.connect()
            logger.info("Connected successfully.")
        except ConnectionException as e:
            logger.error(f"ConnectionException: Failed to connect: {e}")
        except TimeoutError as e:
            logger.error(f"TimeoutError: Connection timed out: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred during the connection: {e}")

    def get_function_profiles(self) -> dict[str, FunctionProfile]:
        return self._function_profiles

    def device_information(self) -> DeviceInformation:
        return self._device_information

    async def getval(self, fp_name, dp_name) -> float:
        """
        Reads datapoint value.

        :dp: The already obtained datapoint object

        2 parameters alternative:
        :param fp_name: The name of the functional profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.

        :returns: The current decoded value in the datapoint register.
        """

        try:
            dp = self.find_dp(self.root, fp_name, dp_name)
        except DataPointException as e:
            logger.error(e)
            return float('nan')
        except FunctionalProfileException as e:
            logger.warning(e)
            return float('nan')

        try:
            address = self.get_address(dp)
            size = self.get_size(dp)
            data_type = self.get_datatype(dp)
            reg_type = self.get_register_type(dp)
            slave_id = self.slave_id
            order = self.byte_order
            answer = await self.client.value_decoder(address, size, data_type, reg_type, slave_id, order)
            return answer
        except ClientError as e:
            logger.exception(e)
            return float('nan')

    # TODO under construction
    async def getval_block(self, fp_name: str, dp_name: str):
        try:
            dp = self.find_dp(self.root, fp_name, dp_name)
        except DataPointException as e:
            logger.error(f"DataPointException: {e}")
            return None
        except FunctionalProfileException as e:
            logger.warning(f"FunctionalProfileException: {e}")
            return None

        try:
            address = self.get_address(dp)
            size = self.get_size(dp)
            data_type = self.get_datatype(dp)
            reg_type = self.get_register_type(dp)
            slave_id = self.slave_id
            order = self.byte_order
            answer = await self.client.mult_value_decoder(address, size, data_type, reg_type, slave_id, order)
            return answer
        except ClientError as e:
            logger.exception(f"ClientError: Failed to retrieve value block {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            return None

    async def setval(self, fp_name: str, dp_name: str, value: float) -> None:
        try:
            dp = self.find_dp(self.root, fp_name, dp_name)
        except DataPointException as e:
            logger.error(f"DataPointException: {e}")
            return
        except FunctionalProfileException as e:
            logger.warning(f"FunctionalProfileException: {e}")
            return

        try:
            address = self.get_address(dp)
            data_type = self.get_datatype(dp)
            slave_id = self.slave_id
            order = self.byte_order
            await self.client.value_encoder(address, value, data_type, slave_id, order)
            logger.info(f"Value {value} has been set for {dp_name} in {fp_name}")
        except ClientError as e:
            logger.exception(f"ClientError: Failed to set value {e}")
        except ValueError as e:
            logger.error(f"ValueError: Invalid value or datatype {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")

    def get_device_profile(self):
        try:
            brand_name = self.root.device_information.brand_name
            nominal_power = self.root.device_information.nominal_power
            level_of_operation = self.root.device_information.legible_description

            if None in [brand_name, nominal_power, level_of_operation]:
                raise DeviceInformationError("Incomplete device information")

            logger.info(f"Brand Name: {brand_name}")
            logger.info(f"Nominal Power: {nominal_power}")
            logger.info(f"Level of Operation: {level_of_operation}")

            return self.root.device_information

        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None
        except DeviceInformationError as e:
            logger.error(f"DeviceInformationError: {e}")
            return None

    def get_register_type(self, dp) -> str:
        """
        Returns register type E.g. "HoldRegister"
        :param fp_name: The name of the functional profile
        :param dp_name: The name of the data point.
        :returns: The type of the register
        """
        try:
            register_type = dp.modbus_data_point_configuration.register_type.value
            if register_type is None:
                raise DataProcessingError("Register type is None")
            return register_type
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_datatype(self, dp) -> str:
        try:
            datatype = dp.modbus_data_point_configuration.modbus_data_type.__dict__
            for key in datatype:
                if datatype[key] is not None:
                    return key
            raise DataProcessingError('data_type not available')
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_bit_rank(self, dp):
        try:
            bitrank = dp.modbus_data_point_configuration.bit_rank
            if bitrank is None:
                raise DataProcessingError("Bit rank is None")
            return bitrank
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_address(self, dp):
        try:
            address = dp.modbus_data_point_configuration.address
            if address is None:
                raise DataProcessingError("Address is None")
            return address
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_size(self, dp):
        try:
            size = dp.modbus_data_point_configuration.number_of_registers
            if size is None:
                raise DataProcessingError("Size is None")
            return size
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_multiplicator(self, dp):
        try:
            multiplicator = dp.modbus_attributes.scaling_factor.multiplicator
            if multiplicator is None:
                raise DataProcessingError("Multiplicator is None")
            return multiplicator
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_power_10(self, dp):
        try:
            power_10 = dp.modbus_attributes.scaling_factor.powerof10
            if power_10 is None:
                raise DataProcessingError("Power of 10 is None")
            return power_10
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_unit(self, dp):
        try:
            unit = dp.data_point.unit.value
            if unit is None:
                raise DataProcessingError("Unit is None")
            return unit
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def get_name(self, dp):
        try:
            name = dp.data_point.data_point_name
            if name is None:
                raise DataProcessingError("Name is None")
            return name
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
            return None

    def find_dp(self, root, fp_name: str, dp_name: str):
        """
        Searches the datapoint in the root element.
        :param root: The root element created with the xsdata parser
        :param fp_name: The name of the funcitonal profile in which the datapoint resides
        :param dp_name: The name of the datapoint
        :returns: The datapoint element found in root, if not, returns None.
        """
        fp = next(filter(lambda x: x.functional_profile.functional_profile_name == fp_name,
                         root.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element),
                  None)
        if fp:
            dp = next(
                filter(lambda x: x.data_point.data_point_name == dp_name, fp.data_point_list.data_point_list_element),
                None)
            if dp:
                return dp
            raise DataPointException(f"Datapoint {dp_name} not found in functional profile {fp_name}.")
        raise FunctionalProfileException(f"Functional profile {fp_name} not found in XML file.")

    # TODO a getval for L1, L2 and L3 at the same time

    # TODO
    def get_dp_attribute(self, datapoint: str, attribute: str):
        """
        Searches for a specific attribute in the datapoint via a key.
        :param attribute"address", "size", "bitrank", "data_type", "register_type", "unit", "multiplicator", "power_of", "name"
        :returns: The chosen attribute.
        """
        # TODO
        ...


async def test_loop():
    while True:
        print('start')
        interface_file = 'abb_terra_01.xml'
        sgr_modbus = SgrModbusInterface(interface_file)
        await sgr_modbus.client.client.connect()
        getval = await sgr_modbus.getval('CurrentAC', 'CurrentACL1')
        print(getval)
        await asyncio.sleep(10)


if __name__ == "__main__":
    starting_time = time.time()
    print('start')
    try:
        asyncio.run(test_loop())
    except KeyboardInterrupt:
        print("done")
