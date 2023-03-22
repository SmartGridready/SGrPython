from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any, Iterable
from pymodbus.constants import Endian
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
import time

from sgr_library.data_classes.ei_modbus import SgrModbusDeviceFrame
from sgr_library.data_classes.ei_modbus.sgr_modbus_eidevice_frame import SgrModbusDataPointsFrameType
from sgr_library.modbus_client import SGrModbusClient


def get_address(root) -> str:
    """
    :param root: The root element created with the xsdata parser
    :returns: String with ip address from xml file.
    """
    address = ''
    address += str(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.address.ip_v4n1)
    address += '.'
    address += str(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.address.ip_v4n2)
    address += '.'
    address += str(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.address.ip_v4n3)
    address += '.'
    address += str(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.address.ip_v4n4)
    return address

def get_port(root) -> str:
    """
    :param root: The root element created with the xsdata parser
    :returns: string with port from xml file.
    """
    return(str(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.port))

def get_slave(root) -> int:
    return(int(root.modbus_interface_desc.trsp_srv_modbus_tcpout_of_box.slave_id))

def get_endian(root) -> str:
    endian = str(root.modbus_interface_desc.conversion_scheme[0].value)
    if endian == 'BigEndian':
        return(Endian.Big)
    return(Endian.Little)

def find_dp(root, fp_name: str, dp_name: str) -> SgrModbusDataPointsFrameType:
    """
    Searches the datapoint in the root element.
    :param root: The root element created with the xsdata parser
    :param fp_name: The name of the funcitonal profile in which the datapoint resides
    :param dp_name: The name of the datapoint
    :returns: The datapoint element found in root, if not, returns None.
    """
    fp = next(filter(lambda x: x.functional_profile.profile_name == fp_name, root.fp_list_element), None)
    if fp:
        dp = next(filter(lambda x: x.data_point.datapoint_name == dp_name, fp.dp_list_element), None)
        if dp:
            return dp


class SgrModbusInterface: 

    def __init__(self, xml_file: str) -> None:
        """
        Creates a connection from xml file data.
        Parses the xml file with xsdata library.
        :param xml_file: Name of the xml file to parse
        """
        interface_file = xml_file
        parser = XmlParser(context=XmlContext())
        self.root = parser.parse(interface_file, SgrModbusDeviceFrame)
        #self.root = parser.parse(interface_file, SgrModbusDeviceDescriptionType)
        self.ip = get_address(self.root)
        self.port = get_port(self.root)
        self.client = SGrModbusClient(self.ip, self.port)
        self.slave_id = get_slave(self.root)
        self.byte_order = get_endian(self.root)

    #TODO
    def get_dp_attribute(self, datapoint: str, attribute: str):
        """
        Searches for a specific attribute in the datapoint via a key.
        :param attribute"address", "size", "bitrank", "data_type", "register_type", 
        "unit", "multiplicator", "power_of", "name"
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

    def get_register_type(self, dp: SgrModbusDataPointsFrameType) -> str:
        """
        Returns register type E.g. "HoldRegister"
        :param fp_name: The name of the functional profile
        :param dp_name: The name of the data point.
        :returns: The type of the register 
        """
        register_type = dp.modbus_data_point[0].modbus_first_register_reference.register_type.value
        return register_type

    def get_datatype(self, dp: SgrModbusDataPointsFrameType) -> str:
        datatype = dp.modbus_data_point[0].modbus_data_type.__dict__
        for key in datatype:
            if datatype[key] != None:
                return key
        print('data_type not available')
    
    def get_bit_rank(self, dp: SgrModbusDataPointsFrameType):
        bitrank = dp.modbus_data_point[0].modbus_first_register_reference.bit_rank
        return bitrank

    def get_address(self, dp: SgrModbusDataPointsFrameType):
        address = dp.modbus_data_point[0].modbus_first_register_reference.addr
        return address


    def get_size(self, dp: SgrModbusDataPointsFrameType):
        size = dp.modbus_data_point[0].dp_size_nr_registers
        return size

    def get_multiplicator(self, dp: SgrModbusDataPointsFrameType):
        multiplicator = dp.dp_mb_attr_reference[0].modbus_attr[0].scaling_by_mul_pwr.multiplicator
        return multiplicator

    def get_power_10(self, dp: SgrModbusDataPointsFrameType):
        power_10 = dp.dp_mb_attr_reference[0].modbus_attr[0].scaling_by_mul_pwr.powerof10
        return power_10

    def get_unit(self, dp: SgrModbusDataPointsFrameType):
        unit = dp.data_point[0].unit.value
        return unit

    def get_name(self, dp: SgrModbusDataPointsFrameType):
        name = dp.data_point[0].datapoint_name
        return name

    def find_dp(self, fp_name: str, dp_name: str) -> SgrModbusDataPointsFrameType:
        """
        Searches the datapoint in the root element.
        :param root: The root element created with the xsdata parser
        :param fp_name: The name of the funcitonal profile in which the datapoint resides
        :param dp_name: The name of the datapoint
        :returns: The datapoint element found in root, if not, returns None.
        """
        fp = next(filter(lambda x: x.functional_profile.profile_name == fp_name, root.fp_list_element), None)
        if fp:
            dp = next(filter(lambda x: x.data_point.datapoint_name == dp_name, fp.dp_list_element), None)
            if dp:
                return dp

    # TODO a getval for L1, L2 and L3 at the same time

if __name__ == "__main__":
    starting_time = time.time()
    print('start')
    interface_file = 'SGr_04_0016_xxxx_ABBMeterV0.2.1.xml'
    a = SgrModbusInterface(interface_file)
    #a.setval('ActiveEnerBalanceAC', 'ActiveImportAC', 9000)
    print(a.getval('ActiveEnerBalanceAC', 'ActiveImportAC'))
    dp = find_dp(a.root, 'ActiveEnerBalanceAC', 'ActiveImportAC')
    print(a.getval(dp))
    