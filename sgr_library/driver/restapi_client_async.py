import configparser
import json
import logging
import ssl
from collections.abc import Mapping
from typing import Any

import aiohttp
import certifi
import jmespath
from aiohttp import ClientConnectionError, ClientResponseError
from cachetools import TTLCache
from sgrspecification.generic import DataDirectionProduct, DeviceCategory
from sgrspecification.generic.base_types import ResponseQuery
from sgrspecification.product import (
    DeviceFrame,
    HeaderList,
    HttpMethod,
    RestApiDataPoint,
    RestApiFunctionalProfile,
)
from sgrspecification.product.product import ConfigurationList

from sgr_library.api import (
    BaseSGrInterface,
    ConfigurationParameter,
    DataPoint,
    DataPointProtocol,
    DeviceInformation,
    FunctionProfile,
)
from sgr_library.api.configuration_parameter import (
    build_configurations_parameters,
)
from sgr_library.validators import build_validator

logging.basicConfig(level=logging.ERROR)


def build_rest_data_point(
    data_point: RestApiDataPoint,
    function_profile: RestApiFunctionalProfile,
    interface: "SgrRestInterface",
) -> DataPoint:
    protocol = RestDataPoint(data_point, function_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


class RestDataPoint(DataPointProtocol):
    def __init__(
        self,
        rest_api_dp: RestApiDataPoint,
        rest_api_fp: RestApiFunctionalProfile,
        interface: "SgrRestInterface",
    ):
        self._dp = rest_api_dp
        self._fp = rest_api_fp
        if  self._dp.rest_api_data_point_configuration is None or self._dp.rest_api_data_point_configuration.rest_api_service_call is None:
            raise Exception("illegal")

        self._method = self._dp.rest_api_data_point_configuration.rest_api_service_call.request_method if  self._dp.rest_api_data_point_configuration.rest_api_service_call.request_method else HttpMethod.GET
        self._header = self._dp.rest_api_data_point_configuration.rest_api_service_call.request_header if  self._dp.rest_api_data_point_configuration.rest_api_service_call.request_header else HeaderList()
        self._body = self._dp.rest_api_data_point_configuration.rest_api_service_call.request_body
        self._path = self._dp.rest_api_data_point_configuration.rest_api_service_call.request_path if self._dp.rest_api_data_point_configuration.rest_api_service_call.request_path else ""
        self._query = self._dp.rest_api_data_point_configuration.rest_api_service_call.response_query if self._dp.rest_api_data_point_configuration.rest_api_service_call.response_query else ""

        self._fp_name = ""
        if (
            rest_api_fp.functional_profile is not None
            and rest_api_fp.functional_profile.functional_profile_name
            is not None
        ):
            self._fp_name = (
                rest_api_fp.functional_profile.functional_profile_name
            )

        self._dp_name = ""
        if (
            rest_api_dp.data_point is not None
            and rest_api_dp.data_point.data_point_name is not None
        ):
            self._dp_name = rest_api_dp.data_point.data_point_name

        self._interface = interface

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    async def read(self):
        await self._interface.get_val(self._method, self._path, self._header, self._body, self._query)
        return await self._interface.getval(self._fp_name, self._dp_name)

    async def write(self, data: Any):
        pass

    def direction(self) -> DataDirect
        if (
            self._dp.data_point is None
            or self._dp.data_point.data_direction is None
        ):
            raise Exception("missing data direction")
        return self._dp.data_point.data_direction


class RestFunctionProfile(FunctionProfile):
    def __init__(
        self,
        rest_api_fp: RestApiFunctionalProfile,
        interface: "SgrRestInterface",
    ):
        self._fp = rest_api_fp
        self._interface = interface

        dps = [
            build_rest_data_point(dp, self._fp, self._interface)
            for dp in self._fp.data_point_list.data_point_list_element
        ]
        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        return self._fp.functional_profile.functional_profile_name

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SgrRestInterface(BaseSGrInterface):
    """
    SmartGrid ready External Interface Class for Rest API
    """

    def is_connected(self):
        return self._is_connected

    async def disconnect_async(self):
        self._is_connected = False
        print("todo clean up connection")

    async def connect_async(self):
        await self.authenticate()

    def get_function_profiles(self) -> Mapping[str, FunctionProfile]:
        return self._function_profiles

    def device_information(self) -> DeviceInformation:
        return self._device_information

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configuration_parameters

    def __init__(
        self, frame: DeviceFrame, configuration: configparser.ConfigParser
    ):
        # session
        device_info = frame.device_information
        if device_info is None:
            raise Exception("invalid")

        self._device_information = DeviceInformation(
            name=frame.device_name if frame.device_name else "",
            manufacture=frame.manufacturer_name
            if frame.manufacturer_name
            else "",
            software_revision=device_info.software_revision if device_info.software_revision else "",
            hardware_revision=device_info.hardware_revision if device_info.hardware_revision else "",
            device_category=device_info.device_category if device_info.device_category else DeviceCategory.DEVICE_INFORMATION,
            is_local=device_info.is_local_control if device_info.is_local_control else False,
        )
        self._is_connected = False
        self._configuration_parameters = build_configurations_parameters(
            frame.configuration_list
            if frame.configuration_list
            else ConfigurationList()
        )
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._conntector = aiohttp.TCPConnector(ssl=self._ssl_context)
        self._session = aiohttp.ClientSession(connector=self._conntector)
        self._token = None
        self._root = frame
        self._cache = TTLCache(maxsize=100, ttl=5)

        fps = [
            RestFunctionProfile(profile, self)
            for profile in self._root.interface_list.rest_api_interface.functional_profile_list.functional_profile_list_element
        ]
        self._function_profiles = {fp.name(): fp for fp in fps}
        try:
            description = self._root.interface_list.rest_api_interface.rest_api_interface_description
            request_body = str(
                description.rest_api_bearer.rest_api_service_call.request_body
            )
            self.data = json.loads(request_body)
            self.base_url = str(description.rest_api_uri)
            request_path = str(
                description.rest_api_bearer.rest_api_service_call.request_path
            )
            self.authentication_url = f"https://{self.base_url}{request_path}"
            logging.info(f"Authentication URL: {self.authentication_url}")

            self.call = self._root.interface_list.rest_api_interface.rest_api_interface_description.rest_api_bearer.rest_api_service_call
            self.headers = {
                header_entry.header_name: header_entry.value
                for header_entry in self.call.request_header.header
            }
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
        except Exception:
            logging.exception("An unexpected error occurred")
            raise

    async def authenticate(self):
        try:
            async with self._session.post(
                url=self.authentication_url,
                headers=self.headers,
                json=self.data,
            ) as res:
                if 200 <= res.status < 300:
                    logging.info(
                        f"Authentication successful: Status {res.status}"
                    )
                    try:
                        response = await res.text()
                        token = jmespath.search(
                            "accessToken", json.loads(response)
                        )
                        if token:
                            self._token = str(token)
                            logging.info("Token retrieved successfully")
                        else:
                            logging.warning("Token not found in the response")
                            self._is_connected = True
                    except json.JSONDecodeError:
                        logging.error("Failed to decode JSON response")
                    except jmespath.exceptions.JMESPathError:
                        logging.error(
                            "Failed to search JSON data using JMESPath"
                        )
                else:
                    logging.warning(
                        f"Authentication failed: Status {res.status}"
                    )
                    logging.info(f"Response: {await res.text()}")

        except aiohttp.ClientError as e:
            logging.error(f"Network error occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    async def close(self):
        await self._session.close()

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
                    lambda x: x.functional_profile.functional_profile_name
                    == fp_name,
                    root.interface_list.rest_api_interface.functional_profile_list.functional_profile_list_element,
                ),
                None,
            )
        except AttributeError as e:
            logging.error(f"Attribute error encountered: {e}")
            return None

        if fp:
            try:
                dp = next(
                    filter(
                        lambda x: x.data_point.data_point_name == dp_name,
                        fp.data_point_list.data_point_list_element,
                    ),
                    None,
                )
            except AttributeError as e:
                logging.error(f"Attribute error encountered: {e}")
                return None

            if dp:
                return dp
            else:
                logging.error(
                    f"Datapoint '{dp_name}' not found in functional profile '{fp_name}'."
                )
                return None
        else:
            logging.error(f"Functional profile '{fp_name}' not found.")
            return None


    async def get_val(self, method: HttpMethod, request_path: str, headers: HeaderList, body: str | None, query: ResponseQuery):
        try:
            url = f"https://{self.base_url}{request_path}"
            # All headers into dicitonary
            request_headers  = {
                header_entry.header_name: header_entry.value
                for header_entry in headers.header
            }
            request_headers["Authorization"] = f"Bearer {self._token}"

            cache_key = (frozenset(request_headers), url)

            if cache_key in self._cache:
                return self._cache.get(cache_key)
            else:
                async with self._session.request(method.value, url, headers=headers, body=body) as reqeust:
                    reqeust.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                    response = await reqeust.json()
                    logging.info(f"Getval Status: {reqeust.status}")
                    response = json.dumps(response)
                    q = query.query if query.query else ""
                    value = jmespath.search(q, json.loads(response))
                    self._cache[cache_key] = value
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
