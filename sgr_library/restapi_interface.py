import time
import os
import configparser
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext

# Import generated Data Classes
from sgr_library.data_classes.ei_rest_api import SgrRestapideviceDescriptionType
from sgr_library.data_classes.ei_modbus import SgrModbusDeviceDescriptionType

# Smartgrid Ready Libraries
from datetime import datetime, timezone
import jmespath
from sgr_library.modbus_interface import find_dp
from sgr_library.restapi_client import RestapiConnect
from jinja2 import Template


class RestapiInterface():

    def __init__(self, interface_file, private_config):
        self.private_config = private_config
        self.parser = XmlParser(context=XmlContext())
        self.root = self.parser.parse(interface_file, SgrRestapideviceDescriptionType)
        self.communication_channel = RestapiConnect(self.root, private_config)
        self.packet = False
        self.cycle_start_timestamp = time.time()
        self.receivedAt = time.time()

    
    def add_private_config(self, string: str, params) -> str: 
        """
        Auxiliary function that adds te sensor_id number to the following string: "/digitaltwins/{{sensor_id}}"
        """
        jT = Template(string)
        private_config = jT.render(params['RESSOURCE'])
        return private_config

    
    def new_packet(self, private_config, communication_channel, endpoint) -> tuple:
        """
        HTTP get request for a new packet from the communication_channel
        :return: (packet, recieved)
        """
        endpoint = self.add_private_config(endpoint, private_config) # Adds sensor_id to the private config   
        packet = communication_channel.get(endpoint)
        recieved = time.time()
        recievedAt = datetime.fromtimestamp(recieved, timezone.utc)
        return(packet, recieved)

    def check_package(self, dp):
        """
        Checks the time the package was recieved, if it is older than the value, it takes a new one.
        """
        if not self.packet or self.cycle_start_timestamp - self.receivedAt > 10.0:        
            endpoint = dp.rest_apidata_point[0].rest_apiend_point
            self.packet, self.receivedAt = self.new_packet(self.private_config, self.communication_channel, endpoint)

    def datapoint_info(self, fp_name: str, dp_name: str) -> tuple:
        """
        returns all the information contained in the datapoint.
        """
        dp = find_dp(self.root, fp_name, dp_name)
        if dp:
            #Cheks the time the package was recieved, if it is older than the value, it takes a new one.
            self.check_package(dp)
            # We get the datapoint's information
            value = jmespath.search(dp.rest_apidata_point[0].rest_apijmespath, self.packet) # Returns the key value in the jmes packet
            unit = dp.data_point[0].unit.value
            timestamp = time.ctime(self.receivedAt)
            aged = self.cycle_start_timestamp - self.receivedAt
            return value, unit, timestamp, aged
        print('Requested datapoint not found in xml file')

    # get_val function to implement for getting a single value
    def get_val_detailed(self, fp_name: str, dp_name: str) -> float:
        """
        :return: Datapoint value
        """
        datapoint_info = self.datapoint_info(fp_name, dp_name)
        value = datapoint_info[0]
        unit = datapoint_info[1]
        timestamp = datapoint_info[2]
        aged = datapoint_info[3]
        print(f"FP {fp_name} DP {dp_name} value {value} {unit} received at {timestamp} aged {aged :.2f} seconds")
        #TODO raise exception: datapoint not found.

    
    def get_val(self, fp_name: str, dp_name: str) -> tuple:
        """
        :return: Datapoint value
        """
        datapoint_info = self.datapoint_info(fp_name, dp_name)
        return datapoint_info[0]


if __name__ == "__main__":
    print('start')
    interface_file = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
    config_file = 'config_CLEMAPEnMon_ressource_default.ini'

    config_file_path_default = os.path.join( os.path.dirname(os.path.realpath(__file__)), config_file)
    config_ressource = configparser.ConfigParser()
    config_ressource.read(config_file_path_default)
    a = RestapiInterface(interface_file, config_ressource)
    print(a.get_val('ActivePowerAC', 'ActivePowerACtot'))
 

