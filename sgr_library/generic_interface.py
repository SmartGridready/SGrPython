from xml.dom.minidom import Element
from modbus_interface import SgrModbusInterface
from restapi_interface import RestapiInterface
import os
import configparser
import xml.etree.ElementTree as ET


def get_protocol(xml_file:str) -> str:
    """
    Searches for protocol type in xml file
    :return: 
    """
    root = ET.parse(xml_file).getroot()
    element = root.tag
    protocol_type = element.split('}')[1]
    return protocol_type


class GenericInterface(SgrModbusInterface, RestapiInterface):


    def __init__(self, xml_file: str, config=None) -> None:
        """
        Chooses which interface to use from xml file data.
        :param xml_file: Name of the xml file to parse in chosen interface
        """
        self.protocol_type = get_protocol(xml_file)
        self.modbus_protocol = ['SGrModbusDeviceFrame', 'SGrModbusDeviceDescriptionType']
        self.restapi_protocol = ['SGrRESTAPIDeviceDescriptionType']

        if self.protocol_type in self.modbus_protocol:
            SgrModbusInterface.__init__(self, xml_file)
        elif self.protocol_type in self.restapi_protocol:
            RestapiInterface.__init__(self, xml_file, config_file)

    def getval(self, *parameter) -> tuple:
        if self.protocol_type in self.modbus_protocol:
            return(SgrModbusInterface.getval(self, *parameter))
        elif self.protocol_type in self.restapi_protocol:
            return(RestapiInterface.getval(self, *parameter))
        

if __name__ == "__main__":

    energy_monitor_config_file_path_default = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 
        'config_CLEMAPEnMon_ressource_default.ini'
        )
    config_file = configparser.ConfigParser()
    config_file.read(energy_monitor_config_file_path_default)

    interface_file = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
    sgr_component = GenericInterface(interface_file, config_file)
    value = sgr_component.getval('ActivePowerAC', 'ActivePowerACtot')
    print(value)

    interface_file2 = 'SGr_HeatPump_Test.xml'
    sgr_component2 = GenericInterface(interface_file2)
    dp = sgr_component2.find_dp('HeatPumpBase', 'HPOpState')
    sgr_component2.get_device_profile()

    value2 = sgr_component2.getval('HeatPumpBase', 'HPOpState')
    print(value2)