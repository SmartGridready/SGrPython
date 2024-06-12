import logging
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any, Iterable
from pymodbus.constants import Endian
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
import time

from sgr_library.api import build_configurations_parameters
#from sgr_library.data_classes.ei_modbus import SgrModbusDeviceDescriptionType
from sgrspecification.product import DeviceFrame
#from sgr_library.data_classes.ei_modbus.sgr_modbus_eidevice_frame import SgrModbusDataPointsFrameType
from sgr_library.modbusRTU_client import SGrModbusRTUClient
from sgr_library.auxiliary_functions import get_port, get_endian, find_dp, get_baudrate, get_slave_rtu, get_parity



class SgrModbusRtuInterface:
    # a global Modbus client
    globalModbusRTUClient = None

    def __init__(self, frame: DeviceFrame) -> None:
        """
        Creates a connection from xml file data.
        Parses the xml file with xsdata library.
        :param xml_file: Name of the xml file to parse
        """

        self.root = frame
        #self.root = parser.parse(interface_file, SgrModbusDeviceDescriptionType)
        self._configuration_params = build_configurations_parameters(frame.configuration_list)
        self.port = get_port(self.root) #TODO überlegungen machen wo Port untergebracht wird
        self.baudrate = get_baudrate(self.root)
        self.parity = get_parity(self.root)
        self.slave_id = get_slave_rtu(self.root)
        self.byte_order = get_endian(self.root)

        # check if there already exists a ModbusRTUClient for the communication over ModbusRTU
        if SgrModbusRtuInterface.globalModbusRTUClient is None:
            self.client = SGrModbusRTUClient(str(self.port), str(self.parity), int(self.baudrate))
            SgrModbusRtuInterface.globalModbusRTUClient = self.client
        else:
            self.client = SgrModbusRtuInterface.globalModbusRTUClient



    def get_pymodbus_client(self):
        """
        returns the pymodbus client object
        """
        return self.client.client

    #TODO
    def get_dp_attribute(self, datapoint: str, attribute: str):
        """
        Searches for a specific attribute in the datapoint via a key.
        :param attribute"address", "size", "bitrank", "data_type", "register_type", "unit", "multiplicator", "power_of", "name"
        :returns: The chosen attribute.
        """
        #TODO
        ...

    #TODO assign multiple dispatch to the function.
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
    def getval(self, *parameter) -> float:
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

        logging.debug(f"getVal() with address: {address}, size: {size}, data_type:{data_type}, slave_id: {slave_id}, order: {order}") # for debugging
        return self.client.value_decoder(address, size, data_type, reg_type, slave_id, order)

    def setval(self, fp_name: str, dp_name: str, value: float) -> None:
        """
        Writes datapoint value.
        :param fp_name: The name of the funcitonal profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.
        :param value: The value that is to be written on the datapoint.
        """
        dp = find_dp(self.root, fp_name, dp_name)
        address = self.get_address(dp)
        data_type = self.get_datatype(dp)
        slave_id = self.slave_id
        order = self.byte_order
        self.client.value_encoder(address, value, data_type, slave_id, order)

    def get_device_profile(self):
        print(f"Brand Name: {self.root.device_profile.brand_name}")
        print(f"Nominal Power: {self.root.device_profile.nominal_power}")
        print(f"Level of Operation: {self.root.device_profile.dev_levelof_operation}")
        return (self.root.device_profile)

    def get_register_type(self, dp) -> str:
        """
        Returns register type E.g. "HoldRegister"
        :param fp_name: The name of the functional profile
        :param dp_name: The name of the data point.
        :returns: The type of the register
        """
        register_type = dp.modbus_data_point[0].modbus_first_register_reference.register_type.value
        return register_type

    def get_datatype(self, dp) -> str:
        datatype = dp.modbus_data_point[0].modbus_data_type.__dict__
        for key in datatype:
            if datatype[key] != None:
                return key
        print('data_type not available')

    def get_bit_rank(self, dp):
        bitrank = dp.modbus_data_point[0].modbus_first_register_reference.bit_rank
        return bitrank

    def get_address(self, dp):
        address = dp.modbus_data_point[0].modbus_first_register_reference.addr
        return address


    def get_size(self, dp):
        size = dp.modbus_data_point[0].dp_size_nr_registers
        return size

    def get_multiplicator(self, dp)->int:
        multiplicator = dp.modbus_attr[0].scaling_by_mul_pwr.multiplicator
        return multiplicator

    def get_power_10(self, dp)->int:
        power_10 = dp.modbus_attr[0].scaling_by_mul_pwr.powerof10
        return power_10

    def get_unit(self, dp):
        unit = dp.data_point.unit.value
        return unit

    def get_name(self, dp):
        name = dp.data_point[0].datapoint_name
        return name

    def find_dp(self, fp_name: str, dp_name: str):
        """
        Searches the datapoint in the root element.
        :param root: The root element created with the xsdata parser
        :param fp_name: The name of the funcitonal profile in which the datapoint resides
        :param dp_name: The name of the datapoint
        :returns: The datapoint element found in root, if not, returns None.
        """
        for fp in self.root.fp_list_element:
                if fp_name == fp.functional_profile.profile_name:
                    #Secondly we filter the datpoint name
                    for dp in fp.dp_list_element:
                        if dp_name == dp.data_point[0].datapoint_name:
                            return dp
        return None

    def get_device_name(self)-> str:
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
        return self.root.device_profile.dev_name_list.s_manuf_name

    def set_slave_id(self,slave_id: int):
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
    print('ActivePowerACtot :',a.getval('ActivePowerAC', 'ActivePowerACtot'))
    # Power = a.client.value_decoder(0x5B14,2,"int32","HoldingRegister",1,Endian.Big)
    # print(str(Power*0.01) + "W")


    #a.setval('ActiveEnerBalanceAC', 'ActiveImportAC', 9000)

    dp = find_dp(a.root, 'ActiveEnerBalanceAC', 'ActiveImportAC')
    print("ActiveImportAC :",a.getval(dp))

    a.client.client.close()
    print("print finished")
