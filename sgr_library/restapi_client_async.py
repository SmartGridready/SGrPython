import aiohttp
import configparser
import asyncio
import json
import jmespath
import os
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext

from sgr_library.data_classes.ei_rest_api import SgrRestApidataPointType, SgrRestApideviceFrame

from typing import Any, Optional

def find_dp(root, fp_name: str, dp_name: str) -> Optional[SgrRestApidataPointType]:
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

class SgrRestInterface():
    """
    SmartGrid ready External Interface Class for Rest API
    """

    def __init__(self, xml_file, config_file):
        #session
        self.session = aiohttp.ClientSession()
        self.token = None

        #xsd parser and file directory
        parser = XmlParser(context=XmlContext())
        interface_file = xml_file
        self.root = parser.parse(interface_file, SgrRestApideviceFrame)

        #config file
        private_config = config_file
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), private_config)
        parser = configparser.ConfigParser()
        parser.read(config_file_path)
        user = parser.get('AUTHENTICATION', 'username', fallback=None)
        password = parser.get('AUTHENTICATION', 'password', fallback=None)
        self.sensor_id = parser.get('RESSOURCE', 'sensor_id', fallback=None)

        #TODO this one can be formulated more elegantly with a format() method.
        request_body = str(self.root.rest_apiinterface_desc.rest_apibearer.service_call.request_body)
        data = json.loads(request_body)
        data['email'] = user
        data['password'] = password
        self.data = json.dumps(data)

        #authentication url
        self.base_url = str(self.root.rest_apiinterface_desc.trsp_srv_rest_uriout_of_box)
        request_path = str(self.root.rest_apiinterface_desc.rest_apibearer.service_call.request_path) #/authentication
        self.authentication_url = 'https://' + self.base_url + request_path 
        print(self.authentication_url)

        #headers
        self.call = self.root.rest_apiinterface_desc.rest_apibearer.service_call
        self.content = self.call.request_header.header[0].value

        # We add all the headers in the xml file using dictionary comprehension
        self.headers = {header_entry.header_name: header_entry.value for header_entry in self.call.request_header.header}

    async def authenticate(self):
        async with self.session.post(url=self.authentication_url, headers=self.headers, data =self.data) as res:
            if res.status == 201:
                print(f"AUTHENTICATION: {res.status}")
                response = await res.text()
                token = jmespath.search('accessToken', json.loads(response))
                self.token = str(token)
            else:
                print(f"AUTHENTICATION: {res.status}")
                print(f"RESPONSE: {res}")


    async def getval(self, fp_name, dp_name):
        dp = find_dp(self.root, fp_name, dp_name)
        request_path = dp.rest_apidata_point[0].rest_service_call.request_path
        url = 'https://' + str(self.base_url) + str(request_path)
        url = url.format(sensor_id=self.sensor_id)
        #TODO add the queryType into an if statement...
        query = str(dp.rest_apidata_point[0].rest_service_call.response_query.query)

        # Headers dictionary
        headers = {header_entry.header_name: header_entry.value for header_entry in dp.rest_apidata_point[0].rest_service_call.request_header.header}     
        #TODO fix reeplacement of bearerToken variable
        headers['Authorization'] = 'Bearer ' + self.token

        async with self.session.get(url=url, headers=headers) as res:
            print(f"GETVAL: {res.status}")
            response = await res.json()
            response = json.dumps(response)
            value = jmespath.search(query, json.loads(response))
            return value

async def test():
    interface_file = "SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml"
    private_config = "config_CLEMAPEnMon_ressource_default.ini"
    client = SgrRestInterface(interface_file, private_config)
    token = await client.authenticate()
    a = await asyncio.gather(client.getval('ActivePowerAC', 'ActivePowerACL1'))
    print(a)
    await asyncio.sleep(1)
    print('1')
    await asyncio.sleep(1)
    print('2')
    await asyncio.sleep(1)
    print('3')

    #print(find_dp(client.root, 'ActivePowerAC', 'ActivePowerACL1').rest_apidata_point[0].rest_service_call.request_path)
    await client.session.close()

if __name__ == "__main__":
    
    asyncio.run(test())