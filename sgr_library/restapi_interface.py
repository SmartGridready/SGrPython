import time
import os
import configparser
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
from typing import Any, Optional

# Import generated Data Classes
from sgr_library.data_classes.ei_rest_api import SgrRestApidataPointType, SgrRestApideviceFrame
# Smartgrid Ready Libraries
from datetime import datetime, timezone
import jmespath

from sgr_library.restapi_client import RestapiConnect
from jinja2 import Template

"""import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)"""

def find_dp(root, fp_name: str, dp_name: str) -> Optional[SgrRestApidataPointType]:
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
                    if dp_name == dp.data_point.datapoint_name:
                        return dp
    return None


class RestapiInterface():

    def __init__(self, interface_file, private_config):
        self.private_config = private_config
        self.parser = XmlParser(context=XmlContext())
        self.interface_file = interface_file
        self.root = self.parser.parse(self.interface_file, SgrRestApideviceFrame)
        print(self.root.rest_apiinterface_desc.rest_apibearer.service_call.response_query.query)
        #print(self.root.rest_apiinterface_desc.rest_apibearer.rest_apijmespath)
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
        GET http request for a new packet from the communication_channel
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
        if not self.packet or self.cycle_start_timestamp - self.receivedAt > 10.0: #TODO add this to variable config       
            endpoint = dp.rest_apidata_point[0].rest_apiend_point
            self.packet, self.receivedAt = self.new_packet(self.private_config, self.communication_channel, endpoint)

    def datapoint_info(self, fp_name: str, dp_name: str) -> Optional[tuple]:
        """
        returns all the information contained in the datapoint.
        """
        dp = find_dp(self.root, fp_name, dp_name)
        if dp:
            #Cheks the time the package was recieved, if it is older than the value, it takes a new one.
            self.check_package(dp)
            # We get the datapoint's information
            value = jmespath.search(dp.rest_apidata_point[0].rest_apijmespath, self.packet) # Returns the key value in the jmes packet
            unit = dp.data_point.unit.value
            timestamp = time.ctime(self.receivedAt)
            aged = self.cycle_start_timestamp - self.receivedAt
            return value, unit, timestamp, aged
        print('Requested datapoint not found in xml file')

    # get_val function to implement for getting a single value
    def getval_detailed(self, fp_name: str, dp_name: str) -> Optional[tuple]:
        """
        :return: Datapoint value, for example the current in L1
        """
        datapoint_info = self.datapoint_info(fp_name, dp_name)
        value = datapoint_info[0]
        unit = datapoint_info[1]
        timestamp = datapoint_info[2]
        aged = datapoint_info[3]
        print(f"FP {fp_name} DP {dp_name} value {value} {unit} received at {timestamp} aged {aged :.2f} seconds")
        #TODO raise exception: datapoint not found.

    
    def getval(self, fp_name: str, dp_name: str) -> float:
        """
        :return: Datapoint value, for example the current in L1
        """
        datapoint_info = self.datapoint_info(fp_name, dp_name)
        return datapoint_info[0]


    def setval(self, fp_name, dp_name, value):
        dp = find_dp(self.root, fp_name, dp_name)
        if dp:
            hello = dp.rest_apidata_point[0].rest_service_call
            endpoint = dp.rest_apidata_point[0].rest_apiend_point
            return self.communication_channel.post(endpoint, value)
        else:
            print('No dp found')
        # 1) Get information from where to post in the datapoint. 
        # AKA check requestMethod post or patch, and choose function
        # AKA check headers, requestPath, parameters
        # Make request.
        ...


if __name__ == "__main__":




    print('start')
    interface_file = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
    config_file = 'config_CLEMAPEnMon_ressource_default.ini'

    config_file_path_default = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file)
    print(config_file_path_default)
    config_ressource = configparser.ConfigParser()
    config_ressource.read(config_file_path_default)
    a = RestapiInterface(interface_file, config_ressource)
    print(a.getval('ActivePowerAC', 'ActivePowerACtot'))


    body = """{
						"name": "post test",
						"description": "this is a test",
						"address": {{address_value}},
						"coordinates": {{coordinates_vlue}},
						"group_measuring_point": false,
						"sensor_ids": [],
						"user_ids": ["60cc663f6440846788a86cc3"],
						"organization_ids": [],
						"virtual_meter_point": false
			}"""

    #print(a.setval('ActivePowerAC', 'MeterGroup', body))
    #print(a.setval('ActivePowerAC', 'MeterGroup', value1, value2, value3))
    #Setval only defines one value, all others are replaced by configuration.
    #Setarray or Setvalues



