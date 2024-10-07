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
from sgr_specification.v0.generic import DataDirectionProduct, DeviceCategory
from sgr_specification.v0.generic.base_types import ResponseQuery
from sgr_specification.v0.product import (
    DeviceFrame,
    HeaderList,
    HttpMethod,
    RestApiDataPoint,
    RestApiFunctionalProfile,
)
from sgr_specification.v0.product.product import ConfigurationList

from sgr_commhandler.api import (
    BaseSGrInterface,
    ConfigurationParameter,
    DataPoint,
    DataPointProtocol,
    DeviceInformation,
    FunctionProfile,
)
from sgr_commhandler.api.configuration_parameter import (
    build_configurations_parameters,
)
from sgr_commhandler.driver.rest.authentication import setup_authentication
from sgr_commhandler.validators import build_validator

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
        if (
            self._dp.rest_api_data_point_configuration is None
            or self._dp.rest_api_data_point_configuration.rest_api_service_call
            is None
        ):
            raise Exception("illegal")

        self._method = (
            self._dp.rest_api_data_point_configuration.rest_api_service_call.request_method
            if self._dp.rest_api_data_point_configuration.rest_api_service_call.request_method
            else HttpMethod.GET
        )
        self._header = (
            self._dp.rest_api_data_point_configuration.rest_api_service_call.request_header
            if self._dp.rest_api_data_point_configuration.rest_api_service_call.request_header
            else HeaderList()
        )
        self._body = self._dp.rest_api_data_point_configuration.rest_api_service_call.request_body
        self._path = (
            self._dp.rest_api_data_point_configuration.rest_api_service_call.request_path
            if self._dp.rest_api_data_point_configuration.rest_api_service_call.request_path
            else ""
        )
        self._query = (
            self._dp.rest_api_data_point_configuration.rest_api_service_call.response_query
            if self._dp.rest_api_data_point_configuration.rest_api_service_call.response_query
            else ResponseQuery()
        )

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

    async def get_val(self):
        return await self._interface.get_val(
            self._method,
            self._path,
            self._header,
            self._body,
            self._query,
        )

    async def set_val(self, data: Any):
        pass

    def direction(self) -> DataDirectionProduct:
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

        raw_dps = []
        if (
            self._fp.data_point_list
            and self._fp.data_point_list.data_point_list_element
        ):
            raw_dps = self._fp.data_point_list.data_point_list_element

        dps = [
            build_rest_data_point(dp, self._fp, self._interface)
            for dp in raw_dps
        ]

        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        if (
            self._fp.functional_profile
            and self._fp.functional_profile.functional_profile_name
        ):
            return self._fp.functional_profile.functional_profile_name
        return ""

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SgrRestInterface(BaseSGrInterface):
    """
    SmartGrid ready External Interface Class for Rest API
    """

    def __init__(
        self, frame: DeviceFrame, configuration: configparser.ConfigParser
    ):
        device_info = frame.device_information
        if device_info is None:
            raise Exception("invalid")
        self._device_information = DeviceInformation(
            name=frame.device_name if frame.device_name else "",
            manufacture=frame.manufacturer_name
            if frame.manufacturer_name
            else "",
            software_revision=device_info.software_revision
            if device_info.software_revision
            else "",
            hardware_revision=device_info.hardware_revision
            if device_info.hardware_revision
            else "",
            device_category=device_info.device_category
            if device_info.device_category
            else DeviceCategory.DEVICE_INFORMATION,
            is_local=device_info.is_local_control
            if device_info.is_local_control
            else False,
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
        self._root = frame
        self._cache = TTLCache(maxsize=100, ttl=5)

        if (
            self._root.interface_list
            and self._root.interface_list
            and self._root.interface_list.rest_api_interface
        ):
            self._raw_interface = self._root.interface_list.rest_api_interface
        else:
            raise Exception("Invalid")
        desc = self._raw_interface.rest_api_interface_description
        if desc is None:
            raise Exception("illegal")
        self._base_url = desc.rest_api_uri
        if self._base_url is None:
            raise Exception("illegal")

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [RestFunctionProfile(profile, self) for profile in raw_fps]
        self._function_profiles = {fp.name(): fp for fp in fps}

    def is_connected(self):
        return self._is_connected

    async def disconnect_async(self):
        self._is_connected = False

    async def connect_async(self):
        await self.authenticate()

    def get_function_profiles(self) -> Mapping[str, FunctionProfile]:
        return self._function_profiles

    def device_information(self) -> DeviceInformation:
        return self._device_information

    def configuration_parameter(self) -> list[ConfigurationParameter]:
        return self._configuration_parameters

    async def authenticate(self):
        await setup_authentication(self._raw_interface, self._session)

    async def close(self):
        await self._session.close()

    async def get_val(
        self,
        method: HttpMethod,
        request_path: str,
        headers: HeaderList,
        body: str | None,
        query: ResponseQuery,
    ):
        try:
            url = f"https://{self._base_url}{request_path}"
            # All headers into dicitonary
            request_headers = {
                header_entry.header_name: header_entry.value
                for header_entry in headers.header
            }
            cache_key = (frozenset(request_headers), url)
            if cache_key in self._cache:
                return self._cache.get(cache_key)
            else:
                async with self._session.request(
                    method.value, url, headers=request_headers
                ) as reqeust:
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

        return None
