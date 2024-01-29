import aiohttp
import asyncio
import json
import jmespath
import os
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
from aiohttp import ClientResponseError, ClientConnectionError
import logging

from sgr_library.data_classes.product import DeviceFrame

import ssl
import certifi

logging.basicConfig(level=logging.ERROR)


class SgrRestInterface():
    """
    SmartGrid ready External Interface Class for Rest API
    """

    def __init__(self, xml_string):
        # session
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        self.session = aiohttp.ClientSession(connector=self.connector)
        self.token = None

        try:
            # xsd parser and file directory
            parser = XmlParser(context=XmlContext())
            self.root = parser.from_string(xml_string)

            description = self.root.interface_list.rest_api_interface.rest_api_interface_description

            self.data = str(description.rest_api_bearer.rest_api_service_call.request_body)

            self.base_url = str(description.rest_api_uri)
            request_path = str(description.rest_api_bearer.rest_api_service_call.request_path)
            self.authentication_url = f'https://{self.base_url}{request_path}'
            logging.info(f"Authentication URL: {self.authentication_url}")

            self.call = self.root.interface_list.rest_api_interface.rest_api_interface_description.rest_api_bearer.rest_api_service_call
            self.headers = {header_entry.header_name: header_entry.value for header_entry in self.call.request_header.header}

        except FileNotFoundError:
            logging.exception(f"File not found: {xml_file}")
            raise
        except json.JSONDecodeError:
            logging.exception("Error parsing JSON from the XML file")
            raise
        except ValueError as e:
            logging.exception(str(e))
            raise
        except Exception as e:
            logging.exception("An unexpected error occurred")
            raise

    async def authenticate(self):
        try:
            async with self.session.post(url=self.authentication_url, headers=self.headers, data=self.data) as res:
                if 200 <= res.status < 300:
                    logging.info(f"Authentication successful: Status {res.status}")
                    try:
                        response = await res.text()
                        token = jmespath.search('accessToken', json.loads(response))
                        if token:
                            self.token = str(token)
                            logging.info("Token retrieved successfully")
                        else:
                            logging.warning("Token not found in the response")
                    except json.JSONDecodeError:
                        logging.error("Failed to decode JSON response")
                    except jmespath.exceptions.JMESPathError:
                        logging.error("Failed to search JSON data using JMESPath")
                else:
                    logging.warning(f"Authentication failed: Status {res.status}")
                    logging.info(f"Response: {await res.text()}")

        except aiohttp.ClientError as e:
            logging.error(f"Network error occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    async def close(self):
        await self.session.close()
    
    def find_dp(self, root, fp_name: str, dp_name: str):
        """
        Searches the datapoint in the root element.
        :param root: The root element created with the xsdata parser
        :param fp_name: The name of the functional profile in which the datapoint resides
        :param dp_name: The name of the datapoint
        :returns: The datapoint element found in root, if not, returns None.
        """

        if not fp_name or not dp_name:
            raise ValueError("fp_name and dp_name cannot be None or empty")

        try:
            fp = next(
                filter(
                    lambda x: x.functional_profile.functional_profile_name == fp_name, 
                    root.interface_list.rest_api_interface.functional_profile_list.functional_profile_list_element
                ), 
                None
            )
        except AttributeError as e:
            logging.error(f"Attribute error encountered: {e}")
            return None

        if fp:
            try:
                dp = next(
                    filter(
                        lambda x: x.data_point.data_point_name == dp_name, 
                        fp.data_point_list.data_point_list_element
                    ), 
                    None
                )
            except AttributeError as e:
                logging.error(f"Attribute error encountered: {e}")
                return None
            
            if dp:
                return dp
            else:
                logging.error(f"Datapoint '{dp_name}' not found in functional profile '{fp_name}'.")
                return None
        else:
            logging.error(f"Functional profile '{fp_name}' not found.")
            return None

    async def getval(self, fp_name, dp_name):
        try:
            dp = self.find_dp(self.root, fp_name, dp_name)
            if not dp:
                raise ValueError(f"Data point for {fp_name}, {dp_name} not found")

            # Dataclass parsing
            service_call = dp.rest_api_data_point_configuration.rest_api_service_call
            request_path = service_call.request_path

            # Urls string
            url = f'https://{self.base_url}{request_path}'
            
            query = str(service_call.response_query.query)

            # All headers into dicitonary
            headers = {
                header_entry.header_name: header_entry.value
                for header_entry in service_call.request_header.header
            }
            headers['Authorization'] = f'Bearer {self.token}'

            async with self.session.get(url=url, headers=headers) as res:
                res.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                
                response = await res.json()
                logging.info(f"Getval Status: {res.status}")

                response = json.dumps(response)
                value = jmespath.search(query, json.loads(response))
                return value

        except ClientResponseError as e:
            logging.error(f"HTTP error occurred: {e}")
        except ClientConnectionError as e:
            logging.error(f"Connection error occurred: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        return None  # Return None or an appropriate default/fallback value in case of error

async def test():

    interface_file = "SGr_04_mmmm_dddd_CLEMAPEnergyMonitorEIV0.2.1.xml"
    private_config = "config_CLEMAPEnMon_ressource_default.ini"

    client = SgrRestInterface(interface_file, private_config)
    token = await client.authenticate()
    value = await asyncio.gather(client.getval('ActivePowerAC', 'ActivePowerACL1'))
    
    print(value)
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