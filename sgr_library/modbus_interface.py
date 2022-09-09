from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any, Iterable
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
import time

from sgr_library.data_classes.ei_modbus import SgrModbusDeviceDescriptionType
from sgr_library.data_classes.ei_modbus.sgr_modbus_eidevice_frame import SgrModbusDataPointsFrameType
from sgr_library.modbus_connection import ModbusConnect


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

def find_dp(root, fp_name: str, dp_name: str) -> SgrModbusDataPointsFrameType:
    """
    Searches the datapoint in the root element.
    :param root: The root element created with the xsdata parser
    :param fp_name: The name of the funcitonal profile in which the datapoint resides
    :param dp_name: The name of the datapoint
    :returns: The datapoint element found in root, if not, returns None.
    """
    for fp in root.fp_list_element:
            if fp_name == fp.functional_profile.profile_name:
                #Secondly we filter the datpoint name
                for dp in fp.dp_list_element:
                    if dp_name == dp.data_point[0].datapoint_name:
                        return dp
    return None

class ModbusInterface: 

    def __init__(self, xml_file) -> None:
        """
        Creates a connection from xml file data.
        Parses the xml file with xsdata library.
        :param xml_file: Name of the xml file to parse
        """
        interface_file = xml_file
        parser = XmlParser(context=XmlContext())
        self.root = parser.parse(interface_file, SgrModbusDeviceDescriptionType)
        self.ip = get_address(self.root)
        self.port = get_port(self.root)
        self.client = ModbusConnect(self.ip, self.port)

    #TODO
    def get_dp_attribute(self, datapoint: str, attribute: str):
        """
        Searches for a specific attribute in the datapoint via a key.
        :param attribute"address", "size", "bitrank", "data_type", "register_type", "unit", "multiplicator", "power_of", "name"
        :returns: The chosen attribute.
        """
        #TODO
        ...

    def getval(self, fp_name: str, dp_name: str) -> float:
        """
        Reads datapoint value.
        :param fp_name: The name of the funcitonal profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.
        :returns: The current decoded value in the datapoint register.
        """
        datapoint_info = self.datapoint_info(fp_name, dp_name)
        address = int(datapoint_info[0])
        size = int(datapoint_info[1])
        dp = find_dp(self.root, fp_name, dp_name)
        reg_type = self.get_datatype(dp)
        return self.client.value_decoder(address, size, reg_type)

    def setval(self, fp_name: str, dp_name: str, value: float) -> None:
        """
        Writes datapoint value.
        :param fp_name: The name of the funcitonal profile in which the datapoint resides.
        :param dp_name: The name of the datapoint.
        :param value: The value that is to be written on the datapoint.
        """
        datapoint_info = self.datapoint_info(fp_name, dp_name)
        address = int(datapoint_info[0])
        reg_type = 'INT32u' #TODO Regtype from xml file...
        self.client.value_encoder(address, value, reg_type)
    
    def get_register_type(self, fp_name: str, dp_name: str) -> str:
        """
        Returns register type E.g. "HoldRegister"
        :param fp_name: The name of the functional profile
        :param dp_name: The name of the data point.
        :returns: The type of the register 
        """
        #TODO Exception: not found in the xml file
        dp = find_dp(self.root, fp_name, dp_name)
        if dp:
            #TODO Exception: not found in the xml file
            register_type = dp.modbus_data_point[0].modbus_first_register_reference.register_type.value
            return register_type
        print('DP not found')


    def get_datatype(self, dp) -> str:
        datatype = dp.modbus_data_point[0].modbus_data_type.__dict__
        print(datatype)
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


    #Slowly discontinue
    def datapoint_info(self, fp_name: str, dp_name: str) -> Tuple[int, int, int, str, str, int, int]:
        """
        :param fp_name: The name of the functional profile
        :param dp_name: The name of the data point.
        :returns: datapoint information.
        """
        dp = find_dp(self.root, fp_name, dp_name)
        if dp:
            # We fill the searched datapoint information into variables.
            address = self.get_address(dp)            
            size = dp.modbus_data_point[0].dp_size_nr_registers
            bitrank = dp.modbus_data_point[0].modbus_first_register_reference.bit_rank
            register_type = self.get_register_type
            data_type = self.get_datatype(dp)
            unit = dp.data_point[0].unit.value
            multiplicator = dp.dp_mb_attr_reference[0].modbus_attr[0].scaling_by_mul_pwr.multiplicator
            power_of = dp.dp_mb_attr_reference[0].modbus_attr[0].scaling_by_mul_pwr.powerof10
            name = dp.data_point[0].datapoint_name
            return (address, size, bitrank, register_type, unit, multiplicator, power_of, name)
        print('Requested datapoint not found in xml file')
        #TODO raise exception: datapoint not found.

    # TODO a getval for L1, L2 and L3 at the same time
    


if __name__ == "__main__":
    starting_time = time.time()
    print('start')
    print(time.time() - starting_time)
    interface_file = 'SGr_04_0016_xxxx_ABBMeterV0.2.1.xml'
    a = ModbusInterface(interface_file)
    pa = (time.time() - starting_time)
    #a.setval('ActiveEnerBalanceAC', 'ActiveImportAC', 9000)
    print(a.getval('ActiveEnerBalanceAC', 'ActiveImportAC'))
    print(pa)

    