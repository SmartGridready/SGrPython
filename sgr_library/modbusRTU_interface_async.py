import logging
import os
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any, Iterable
from pymodbus.constants import Endian
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
import time

from sgr_library.api import BaseSGrInterface, DeviceInformation, FunctionProfile, DataPointProtocol, DataPoint, \
    build_configurations_parameters, ConfigurationParameter
from sgr_library.auxiliary_functions import find_dp
from sgr_library.converters import build_converter
from sgrspecification.generic import Parity, DataDirectionProduct

# from sgr_library.data_classes.ei_modbus import SgrModbusDeviceDescriptionType
from sgrspecification.product import DeviceFrame, ModbusDataPoint, ModbusFunctionalProfile

from sgr_library.modbusRTU_client_async import SGrModbusRTUClient
from sgr_library.validators import build_validator


def get_port(root) -> str:
    """
    :param root: The root element created with the xsdata parser
    :returns: string with port from xml file.
    """
    return (str(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.port))
    # return(str(root.modbus_interface_desc.trspSrvModbusRTUoutOfBox.port)) #TODO Port datapoint for RTU in XML is not existing


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
            return 'E'
        case _:
            raise NotImplementedError


def build_modbus_rtu_data_point(data_point: ModbusDataPoint, function_profile: ModbusFunctionalProfile,
                                interface: 'SgrModbusRtuInterface') -> DataPoint:
    protocol = ModBusRTUDataPoint(data_point, function_profile, interface)
    converter = build_converter(data_point.data_point.unit)
    validator = build_validator(data_point.data_point.data_type)
    return DataPoint(protocol, converter, validator)


class ModBusRTUDataPoint(DataPointProtocol):

    def __init__(self, modbus_api_dp: ModbusDataPoint, modbus_api_fp: ModbusFunctionalProfile,
                 interface: 'SgrModbusRtuInterface'):
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


class ModBusRTUFunctionProfile(FunctionProfile):

    def __init__(self, modbus_api_fp: ModbusFunctionalProfile, interface: 'SgrModbusRtuInterface'):
        self._fp = modbus_api_fp
        self._interface = interface
        dps = [build_modbus_rtu_data_point(dp, self._fp, self._interface) for dp in
               self._fp.data_point_list.data_point_list_element]
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
        Creates a connection from xml file data.
        Parses the xml file with xsdata library.
        :param xml_file: Name of the xml file to parse
        """
        self.root = frame
        # self.root = parser.parse(interface_file, SgrModbusDeviceDescriptionType)
        self.port = os.getenv("SGR_RTU_PORT")  # get_port(self.root) #TODO überlegungen machen wo Port untergebracht wird
        self._configurations_params = build_configurations_parameters(frame.configuration_list)
        self.baudrate = get_baudrate(self.root)
        self.parity = get_parity(self.root)
        self.slave_id = get_slave(self.root)
        self.byte_order = get_endian(self.root)
        fps = [ModBusRTUFunctionProfile(profile, self) for profile in
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

    def get_pymodbus_client(self):
        """
        returns the pymodbus client object
        """
        return self.client.client

    # TODO
    def get_dp_attribute(self, datapoint: str, attribute: str):
        """
        Searches for a specific attribute in the datapoint via a key.
        :param attribute"address", "size", "bitrank", "data_type", "register_type", "unit", "multiplicator", "power_of", "name"
        :returns: The chosen attribute.
        """
        # TODO
        ...

    # TODO assign multiple dispatch to the function.
    '''def getval(self, fp_name: str, dp_name: str) -> float:
        """
        Reads datapoint value.
        :param fp_name: The name of the funcitonal profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.
        :returns: The current decoded value in the datapoint register.
        """
        dp = find_dp(self.root, fp_name, dp_name)
        address = self.get_address(dp)
        size = self.get_size(dp)
        data_type = self.get_datatype(dp)
        reg_type = self.get_register_type(dp)
        return self.client.value_decoder(address, size, data_type, reg_type)'''

    # getval with multiple dispatching
    async def getval(self, *parameter) -> float:
        """
        Reads datapoint value.

        :dp: The already obtained datapoint object

        2 parameters alternative:
        :param fp_name: The name of the functional profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.

        :returns: The current decoded value in the datapoint register.
        """
        if len(parameter) == 2:
            dp = find_dp(self.root, parameter[0], parameter[1])
        else:
            dp = parameter[0]
        address = self.get_address(dp)
        size = self.get_size(dp)
        data_type = self.get_datatype(dp)
        reg_type = self.get_register_type(dp)
        slave_id = self.slave_id
        order = self.byte_order

        logging.debug(
            f"getVal() with address: {address}, size: {size}, data_type:{data_type}, slave_id: {slave_id}, order: {order}")  # for debugging
        return await self.client.value_decoder(address, size, data_type, reg_type, slave_id, order)

    async def setval(self, fp_name: str, dp_name: str, value: float) -> None:
        """
        Writes datapoint value.
        :param fp_name: The name of the funcitonal profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.
        :param value: The value that is to be written on the datapoint.
        """
        dp: ModbusDataPoint = find_dp(self.root, fp_name, dp_name)
        address = self.get_address(dp)
        data_type = self.get_datatype(dp)
        slave_id = self.slave_id
        order = self.byte_order
        await self.client.value_encoder(address, value, data_type, slave_id, order)

    def get_device_profile(self):
        return (self.root.device_profile)

    def get_register_type(self, dp: ModbusDataPoint) -> str:
        """
        Returns register type E.g. "HoldRegister"
        :param fp_name: The name of the functional profile
        :param dp_name: The name of the data point.
        :returns: The type of the register
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

    def get_multiplicator(self, dp: ModbusDataPoint) -> int:
        return dp.modbus_attributes.scaling_factor.multiplicator

    def get_power_10(self, dp: ModbusDataPoint) -> int:
        return dp.modbus_attributes.scaling_factor.powerof10

    def get_unit(self, dp: ModbusDataPoint):
        return dp.data_point.unit.value

    def get_name(self, dp: ModbusDataPoint):
        return dp.data_point.data_point_name

    """
    def find_dp(self, fp_name: str, dp_name: str) -> SgrModbusDataPointType:
        
        Searches the datapoint in the root element.
        :param root: The root element created with the xsdata parser
        :param fp_name: The name of the funcitonal profile in which the datapoint resides
        :param dp_name: The name of the datapoint
        :returns: The datapoint element found in root, if not, returns None.
        
        for fp in self.root.fp_list_element:
                if fp_name == fp.functional_profile.profile_name:
                    #Secondly we filter the datpoint name
                    for dp in fp.dp_list_element:
                        if dp_name == dp.data_point[0].datapoint_name:
                            return dp
        return None
    """

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configurations_params

    async def connect(self):
        # check if there already exists a ModbusRTUClient for the communication over ModbusRTU
        if SgrModbusRtuInterface.globalModbusRTUClient is None:
            self.client = SGrModbusRTUClient(str(self.port), str(self.parity), int(self.baudrate))
            SgrModbusRtuInterface.globalModbusRTUClient = self.client
        else:
            self.client = SgrModbusRtuInterface.globalModbusRTUClient

        if self.client:
            connected = await self.client.connect()
            if connected:
                print("Connected to ModbusRTU on Port: " + self.port)

    def get_function_profiles(self) -> dict[str, FunctionProfile]:
        return self._function_profiles

    def device_information(self) -> DeviceInformation:
        return self._device_information

    def find_dp(self, fp_name: str, dp_name: str):
        """
        Searches the datapoint in the root element.
        :param root: The root element created with the xsdata parser
        :param fp_name: The name of the funcitonal profile in which the datapoint resides
        :param dp_name: The name of the datapoint
        :returns: The datapoint element found in root, if not, returns None.
        """
        fp = next(filter(lambda x: x.functional_profile.profile_name == fp_name, self.root.fp_list_element), None)
        if fp:
            dp = next(filter(lambda x: x.data_point.datapoint_name == dp_name, fp.dp_list_element), None)
            if dp:
                return dp

    def get_device_name(self) -> str:
        """
        returns the s_LV1_Name of the device
        """
        return self.root.device_profile.dev_name_list.s_lv1_name

    def get_modbusInterfaceSelection(self) -> str:
        """
        Returns selected Modbus Interface in XML file
        """
        return (self.root.modbus_interface_desc.modbus_interface_selection.value)

    def get_manufacturer(self):
        """
        returns the manufacturer name of the device
        """
        # TODO it could also be root.device_information.alternative_names.manuf_name
        return self.root.manufacturer_name

    def set_slave_id(self, slave_id: int):
        """
        changes the slave id for the instance
        """
        self.slave_id = slave_id

    # TODO a getval for L1, L2 and L3 at the same time


if __name__ == "__main__":
    starting_time = time.time()
    print('start')
    interface_file = '../xml_files/SGr_04_0016_xxxx_ABBMeterV0.2.1.xml'
    a = SgrModbusRtuInterface(interface_file)
    print('ActivePowerACtot :', a.getval('ActivePowerAC', 'ActivePowerACtot'))
    # Power = a.client.value_decoder(0x5B14,2,"int32","HoldingRegister",1,Endian.Big)
    # print(str(Power*0.01) + "W")

    # a.setval('ActiveEnerBalanceAC', 'ActiveImportAC', 9000)

    dp = find_dp(a.root, 'ActiveEnerBalanceAC', 'ActiveImportAC')
    print("ActiveImportAC :", a.getval(dp))

    a.client.client.close()
    print("print finished")
