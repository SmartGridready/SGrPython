import configparser
import json
import logging
import ssl
from typing import Any

import aiohttp
import certifi
import jmespath
from aiohttp import ClientResponseError, ClientConnectionError
from cachetools import TTLCache

from generated.product import RestApiAuthenticationMethod
from sgr_library.api import BaseSGrInterface, FunctionProfile, DataPoint, DataPointProtocol, DeviceInformation, \
    ConfigurationParameter
from sgr_library.api.configuration_parameter import build_configurations_parameters
from sgr_library.converters import build_converter
from sgrspecification.generic import DataDirectionProduct
from sgrspecification.product import DeviceFrame
from sgrspecification.product import RestApiFunctionalProfile, RestApiDataPoint
from sgr_library.validators import build_validator

logging.basicConfig(level=logging.ERROR)


def build_rest_data_point(data_point: RestApiDataPoint, function_profile: RestApiFunctionalProfile,
                          interface: 'SgrRestInterface') -> DataPoint:
    protocol = RestDataPoint(data_point, function_profile, interface)
    converter = build_converter(data_point.data_point.unit)
    validator = build_validator(data_point.data_point.data_type)
    return DataPoint(protocol, converter, validator)


class RestDataPoint(DataPointProtocol):

    def __init__(self, rest_api_dp: RestApiDataPoint, rest_api_fp: RestApiFunctionalProfile,
                 interface: 'SgrRestInterface'):
        self._dp = rest_api_dp
        self._fp = rest_api_fp
        self._interface = interface

    def name(self) -> tuple[str, str]:
        return self._fp.functional_profile.functional_profile_name, self._dp.data_point.data_point_name

    async def read(self):
        return await self._interface.getval(self.name()[0], self.name()[1])

    async def write(self, data: Any):
        pass

    def direction(self) -> DataDirectionProduct:
        return self._dp.data_point.data_direction


class RestFunctionProfile(FunctionProfile):

    def __init__(self, rest_api_fp: RestApiFunctionalProfile, interface: 'SgrRestInterface'):
        self._fp = rest_api_fp
        self._interface = interface

        dps = [build_rest_data_point(dp, self._fp, self._interface) for dp in
               self._fp.data_point_list.data_point_list_element]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp.functional_profile.functional_profile_name

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SgrRestInterface(BaseSGrInterface):
    """
    SmartGrid ready External Interface Class for Rest API
    """

    async def connect(self):
        await self.authenticate()

    def get_function_profiles(self) -> dict[str, FunctionProfile]:
        return self._function_profiles

    def device_information(self) -> DeviceInformation:
        return self._device_information

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configuration_parameters

    def __init__(self, frame: DeviceFrame, configuration: configparser.ConfigParser):
        # session
        self._device_information = DeviceInformation(
            name=frame.device_name,
            manufacture=frame.manufacturer_name,
            software_revision=frame.device_information.software_revision,
            hardware_revision=frame.device_information.hardware_revision,
            device_category=frame.device_information.device_category,
            is_local=frame.device_information.is_local_control
        )
        self._configuration_parameters = build_configurations_parameters(frame.configuration_list)
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        self.session = aiohttp.ClientSession(connector=self.connector)
        self.token = None
        self.root = frame
        self._cache = TTLCache(maxsize=100, ttl=5)

        fps = [RestFunctionProfile(profile, self) for profile in
               self.root.interface_list.rest_api_interface.functional_profile_list.functional_profile_list_element]
        self._function_profiles = {fp.name(): fp for fp in fps}
        try:
            description = self.root.interface_list.rest_api_interface.rest_api_interface_description
            request_body = str(description.rest_api_bearer.rest_api_service_call.request_body)
            self.data = json.loads(request_body)
            self.base_url = str(description.rest_api_uri)
            request_path = str(description.rest_api_bearer.rest_api_service_call.request_path)
            self.authentication_url = f'https://{self.base_url}{request_path}'
            logging.info(f"Authentication URL: {self.authentication_url}")

            self.call = self.root.interface_list.rest_api_interface.rest_api_interface_description.rest_api_bearer.rest_api_service_call
            self.headers = {header_entry.header_name: header_entry.value for header_entry in
                            self.call.request_header.header}
        except json.JSONDecodeError:
            logging.exception("Error parsing JSON from the XML file")
            raise
        except configparser.ParsingError:
            logging.exception("Error parsing the configuration file")
            raise
        except configparser.Error:
            logging.exception("General error reading configuration file")
            raise
        except ValueError as e:
            logging.exception(str(e))
            raise
        except Exception as e:
            logging.exception("An unexpected error occurred")
            raise

    async def authenticate(self):
        try:
            async with self.session.post(url=self.authentication_url, headers=self.headers, json=self.data) as res:
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

            cache_key = (frozenset(headers), url)

            if cache_key in self._cache:
                response = self._cache.get(cache_key)
            else:
                async with self.session.get(url=url, headers=headers) as res:
                    res.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                    response = await res.json()
                    logging.info(f"Getval Status: {res.status}")

                    response = json.dumps(response)
                    self._cache[cache_key] = response

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
