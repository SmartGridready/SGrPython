import configparser
import json
import ssl
from collections.abc import Mapping
from typing import Any
import logging
import aiohttp
import certifi
import jmespath
from aiohttp import ClientConnectionError, ClientResponseError
from cachetools import TTLCache
from sgr_specification.v0.generic import DataDirectionProduct
from sgr_specification.v0.generic.base_types import ResponseQuery
from sgr_specification.v0.product import (
    DeviceFrame,
    HeaderList,
    HttpMethod,
    RestApiDataPoint,
    RestApiFunctionalProfile,
)
from sgr_commhandler.api import (
    SGrBaseInterface,
    DataPoint,
    DataPointProtocol,
    FunctionalProfile,
)
from sgr_commhandler.driver.rest.authentication import setup_authentication
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def build_rest_data_point(
    data_point: RestApiDataPoint,
    function_profile: RestApiFunctionalProfile,
    interface: "SGrRestInterface",
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
        dp_spec: RestApiDataPoint,
        fp_spec: RestApiFunctionalProfile,
        interface: "SGrRestInterface",
    ):
        self._dp_spec = dp_spec
        self._fp_spec = fp_spec
        if (
            self._dp_spec.rest_api_data_point_configuration is None
            or self._dp_spec.rest_api_data_point_configuration.rest_api_service_call is None
            or self._dp_spec.rest_api_data_point_configuration.rest_api_read_service_call is None
            or self._dp_spec.rest_api_data_point_configuration.rest_api_write_service_call is None
        ):
            raise Exception("REST service call configuration missing")

        self._method = (
            self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_method
            if self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_method
            else HttpMethod.GET
        )
        self._header = (
            self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_header
            if self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_header
            else HeaderList()
        )
        self._body = self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_body
        self._path = (
            self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_path
            if self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.request_path
            else ""
        )
        self._query = (
            self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.response_query
            if self._dp_spec.rest_api_data_point_configuration.rest_api_service_call.response_query
            else ResponseQuery()
        )

        self._fp_name = ""
        if (
            fp_spec.functional_profile is not None
            and fp_spec.functional_profile.functional_profile_name
            is not None
        ):
            self._fp_name = (
                fp_spec.functional_profile.functional_profile_name
            )

        self._dp_name = ""
        if (
            dp_spec.data_point is not None
            and dp_spec.data_point.data_point_name is not None
        ):
            self._dp_name = dp_spec.data_point.data_point_name

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
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception("missing data direction")
        return self._dp_spec.data_point.data_direction


class RestFunctionalProfile(FunctionalProfile):
    def __init__(
        self,
        fp_spec: RestApiFunctionalProfile,
        interface: "SGrRestInterface",
    ):
        self._fp_spec = fp_spec
        self._interface = interface

        raw_dps = []
        if (
            self._fp_spec.data_point_list
            and self._fp_spec.data_point_list.data_point_list_element
        ):
            raw_dps = self._fp_spec.data_point_list.data_point_list_element

        dps = [
            build_rest_data_point(dp, self._fp_spec, self._interface)
            for dp in raw_dps
        ]

        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        if (
            self._fp_spec.functional_profile
            and self._fp_spec.functional_profile.functional_profile_name
        ):
            return self._fp_spec.functional_profile.functional_profile_name
        return ""

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points


class SGrRestInterface(SGrBaseInterface):
    """
    SmartGridready External Interface Class for Rest API
    """

    def __init__(
        self, frame: DeviceFrame, configuration: configparser.ConfigParser
    ):
        super().__init__(frame, configuration)

        self._session = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._connector = aiohttp.TCPConnector(ssl=self._ssl_context)
        self._cache = TTLCache(maxsize=100, ttl=5)

        if (
            self._root_spec.interface_list
            and self._root_spec.interface_list
            and self._root_spec.interface_list.rest_api_interface
        ):
            self._raw_interface = self._root_spec.interface_list.rest_api_interface
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
        fps = [RestFunctionalProfile(profile, self) for profile in raw_fps]
        self._function_profiles = {fp.name(): fp for fp in fps}

    def is_connected(self):
        return self._session is not None and not self._session.closed

    async def disconnect_async(self):
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None

    async def connect_async(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(connector=self._connector)
            await self.authenticate()

    def get_function_profiles(self) -> Mapping[str, FunctionalProfile]:
        return self._function_profiles

    async def authenticate(self):
        await setup_authentication(self._raw_interface, self._session)

    async def get_val(
        self,
        method: HttpMethod,
        request_path: str,
        headers: HeaderList,
        body: str | None,
        query: ResponseQuery,
    ):
        try:
            url = f"{self._base_url}{request_path}"
            # All headers into dictionary
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
                    logger.info(f"Getval Status: {reqeust.status}")
                    response = json.dumps(response)
                    q = query.query if query.query else ""
                    value = jmespath.search(q, json.loads(response))
                    self._cache[cache_key] = value
                    return value

        except ClientResponseError as e:
            logger.error(f"HTTP error occurred: {e}")
        except ClientConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        return None
