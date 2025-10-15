"""
Provides the HTTP/REST interface implementation.
"""

import json
import logging
import re
import ssl
from typing import Any, Optional

import aiohttp
import certifi
import jmespath
from aiohttp import ClientConnectionError, ClientResponseError
from cachetools import TTLCache
from multidict import CIMultiDict
from sgr_specification.v0.generic import DataDirectionProduct, Units
from sgr_specification.v0.generic.base_types import ResponseQueryType
from sgr_specification.v0.product import (
    DeviceFrame,
    HeaderList,
    HttpMethod,
)
from sgr_specification.v0.product import (
    RestApiDataPoint as RestApiDataPointSpec,
)
from sgr_specification.v0.product import (
    RestApiFunctionalProfile as RestApiFunctionalProfileSpec,
)
from sgr_specification.v0.product.rest_api_types import (
    ParameterList,
    RestApiServiceCall,
)
from sgr_commhandler.api.data_point_api import (
    DataPoint,
    DataPointProtocol,
)
from sgr_commhandler.api.functional_profile_api import (
    FunctionalProfile
)
from sgr_commhandler.api.device_api import (
    SGrBaseInterface
)
from sgr_commhandler.api.dynamic_parameter import (
    DynamicParameter,
    build_dynamic_parameters,
    build_dynamic_parameter_substitutions
)
from sgr_commhandler.driver.rest.request import (
    RestRequest,
    RestResponse,
    build_rest_request
)
from sgr_commhandler.driver.rest.authentication import setup_authentication
from sgr_commhandler.validators import build_validator
from sgr_commhandler.utils import jmespath_mapping, template

logger = logging.getLogger(__name__)


def build_rest_data_point(
    data_point: RestApiDataPointSpec,
    functional_profile: RestApiFunctionalProfileSpec,
    interface: 'SGrRestInterface',
) -> DataPoint:
    protocol = RestDataPoint(data_point, functional_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


class RestDataPoint(DataPointProtocol[RestApiDataPointSpec]):
    """
    Implements a data point of a REST API interface.
    """

    def __init__(
        self,
        dp_spec: RestApiDataPointSpec,
        fp_spec: RestApiFunctionalProfileSpec,
        interface: 'SGrRestInterface',
    ):
        self._dp_spec = dp_spec
        self._fp_spec = fp_spec

        dp_config = self._dp_spec.rest_api_data_point_configuration
        if not dp_config:
            raise Exception('REST service call configuration missing')

        self._read_call: RestApiServiceCall = RestApiServiceCall()
        self._write_call: RestApiServiceCall = RestApiServiceCall()

        if len(dp_config.rest_api_read_service_call) > 0:
            service_call = dp_config.rest_api_read_service_call[0]
            self._read_call = RestApiServiceCall(
                request_method=(
                    service_call.request_method
                    if service_call.request_method
                    else HttpMethod.GET
                ),
                request_path=(
                    service_call.request_path
                    if service_call.request_path
                    else ''
                ),
                request_header=(
                    service_call.request_header
                    if service_call.request_header
                    else HeaderList()
                ),
                request_query=(
                    service_call.request_query
                    if service_call.request_query
                    else ParameterList()
                ),
                request_form=(
                    service_call.request_form
                    if service_call.request_form
                    else ParameterList()
                ),
                response_query=(
                    service_call.response_query
                    if service_call.response_query
                    else None
                ),
            )
        elif dp_config.rest_api_service_call:
            # old spec, for compatibility reasons
            self._read_call = RestApiServiceCall(
                request_method=(
                    dp_config.rest_api_service_call.request_method
                    if dp_config.rest_api_service_call.request_method
                    else HttpMethod.GET
                ),
                request_path=(
                    dp_config.rest_api_service_call.request_path
                    if dp_config.rest_api_service_call.request_path
                    else ''
                ),
                request_header=(
                    dp_config.rest_api_service_call.request_header
                    if dp_config.rest_api_service_call.request_header
                    else HeaderList()
                ),
                request_query=(
                    dp_config.rest_api_service_call.request_query
                    if dp_config.rest_api_service_call.request_query
                    else ParameterList()
                ),
                request_form=(
                    dp_config.rest_api_service_call.request_form
                    if dp_config.rest_api_service_call.request_form
                    else ParameterList()
                ),
                response_query=(
                    dp_config.rest_api_service_call.response_query
                    if dp_config.rest_api_service_call.response_query
                    else None
                ),
            )

        if len(dp_config.rest_api_write_service_call) > 0:
            service_call = dp_config.rest_api_write_service_call[0]
            self._write_call = RestApiServiceCall(
                request_method=(
                    service_call.request_method
                    if service_call.request_method
                    else HttpMethod.GET
                ),
                request_path=(
                    service_call.request_path
                    if service_call.request_path
                    else ''
                ),
                request_header=(
                    service_call.request_header
                    if service_call.request_header
                    else HeaderList()
                ),
                request_query=(
                    service_call.request_query
                    if service_call.request_query
                    else ParameterList()
                ),
                request_form=(
                    service_call.request_form
                    if service_call.request_form
                    else ParameterList()
                ),
                response_query=(
                    service_call.response_query
                    if service_call.response_query
                    else None
                ),
            )

        if not self._read_call and not self._write_call:
            raise Exception('No REST service call configured')

        self._dynamic_parameters = build_dynamic_parameters(
            self._dp_spec.data_point.parameter_list
            if self._dp_spec.data_point
            else None
        )

        self._fp_name = ''
        if (
            fp_spec.functional_profile is not None
            and fp_spec.functional_profile.functional_profile_name is not None
        ):
            self._fp_name = fp_spec.functional_profile.functional_profile_name

        self._dp_name = ''
        if (
            dp_spec.data_point is not None
            and dp_spec.data_point.data_point_name is not None
        ):
            self._dp_name = dp_spec.data_point.data_point_name

        self._interface = interface

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    def get_specification(self) -> RestApiDataPointSpec:
        return self._dp_spec

    async def get_val(self, parameters: Optional[dict[str, str]] = None, skip_cache: bool = False) -> Any:
        if not self._read_call:
            raise Exception('No read call')

        substitutions = build_dynamic_parameter_substitutions(self._dynamic_parameters, parameters)

        request = build_rest_request(self._read_call, str(self._interface.base_url), substitutions)

        response = await self._interface.execute_request(request, skip_cache)
        if not response.body:
            return None
        if (
            self._read_call.response_query
            and self._read_call.response_query.query_type == ResponseQueryType.JMESPATH_EXPRESSION
        ):
            # JMESPath expression
            query_expression = template.substitute(
                self._read_call.response_query.query if self._read_call.response_query.query else '',
                substitutions
            )
            return jmespath.search(query_expression, json.loads(response.body))
        elif (
            self._read_call.response_query
            and self._read_call.response_query.query_type == ResponseQueryType.JMESPATH_MAPPING
        ):
            # JMESPath mappings
            mappings = self._read_call.response_query.jmes_path_mappings.mapping if self._read_call.response_query.jmes_path_mappings else []
            return jmespath_mapping.map_json_response(response.body, mappings)
        elif (
            self._read_call.response_query
            and self._read_call.response_query.query_type == ResponseQueryType.REGULAR_EXPRESSION
        ):
            # regex
            query_expression = self._read_call.response_query.query if self._read_call.response_query.query else ''
            query_match = re.match(query_expression, response.body)
            if query_match is not None:
                return query_match.group()

        # plain response
        ret_value = response.body

        # apply value mappings
        if self._read_call.value_mapping:
            mappings = self._read_call.value_mapping.mapping
            for m in mappings:
                if m.device_value == ret_value:
                    ret_value = m.generic_value
                    break

        # convert to DP units
        if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.unit_conversion_multiplicator
            and self._dp_spec.data_point.unit_conversion_multiplicator != 1.0
        ):
            ret_value = (
                float(str(ret_value))
                * self._dp_spec.data_point.unit_conversion_multiplicator
            )

        return ret_value

    async def set_val(self, value: Any):
        if not self._write_call:
            raise Exception('No write call')

        # convert to device units
        unit_conv_factor = self._dp_spec.data_point.unit_conversion_multiplicator if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.unit_conversion_multiplicator
        ) else 1.0
        if unit_conv_factor != 1.0:
            value = float(value) / unit_conv_factor

        # apply value mappings
        value = str(value)
        if self._read_call.value_mapping:
            mappings = self._read_call.value_mapping.mapping
            for m in mappings:
                if m.generic_value == value:
                    value = m.device_value
                    break
        # add value to substitutions
        substitutions = {
            'value': value
        }
        request = build_rest_request(self._write_call, str(self._interface.base_url), substitutions=substitutions)
        # TODO use response body
        await self._interface.execute_request(request, skip_cache=True)

    def direction(self) -> DataDirectionProduct:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction

    def unit(self) -> Units:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.unit is None
        ):
            return Units.NONE
        return self._dp_spec.data_point.unit

    def dynamic_parameters(self) -> list[DynamicParameter]:
        return self._dynamic_parameters


class RestFunctionalProfile(FunctionalProfile):
    """
    Implements a functional profile of a REST API interface.
    """

    def __init__(
        self,
        fp_spec: RestApiFunctionalProfileSpec,
        interface: 'SGrRestInterface',
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
        return ''

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points

    def get_specification(self) -> RestApiFunctionalProfileSpec:
        return self._fp_spec


class SGrRestInterface(SGrBaseInterface):
    """
    Implements a REST API device interface.
    """

    def __init__(
        self, frame: DeviceFrame
    ):
        super().__init__(frame)
        self._session = None
        self._cache = TTLCache(maxsize=100, ttl=5)

        if (
            self.device_frame.interface_list
            and self.device_frame.interface_list
            and self.device_frame.interface_list.rest_api_interface
        ):
            self._raw_interface = self.device_frame.interface_list.rest_api_interface
        else:
            raise Exception('No REST interface')
        desc = self._raw_interface.rest_api_interface_description
        if desc is None:
            raise Exception('No REST interface description')
        self.base_url = desc.rest_api_uri
        if self.base_url is None:
            raise Exception('Invalid base URL')
        ssl_verify = (desc.rest_api_verify_certificate.strip().lower() == 'true') if desc.rest_api_verify_certificate is not None else True
        if ssl_verify:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            self._connector = aiohttp.TCPConnector(ssl=ssl_context)
        else:
            self._connector = aiohttp.TCPConnector(verify_ssl=False)

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [RestFunctionalProfile(profile, self) for profile in raw_fps]
        self.functional_profiles = {fp.name(): fp for fp in fps}

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

    async def authenticate(self):
        if self._session:
            await setup_authentication(self._raw_interface, self._session)

    async def execute_request(
        self, request: RestRequest, skip_cache: bool
    ) -> RestResponse:
        try:
            if self._session is None:
                raise Exception('no connection to device established')

            cache_key = (frozenset(request.headers), request.url)
            if not skip_cache and cache_key in self._cache:
                return self._cache[cache_key]

            async with self._session.request(
                request.method,
                request.url,
                headers=request.headers,
                params=request.query_parameters,
                data=request.body
            ) as req:
                req.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                logger.debug(f'execute_request status: {req.status}')
                res_body = await req.text()

                res_headers = CIMultiDict()
                for name, value in req.headers.items():
                    res_headers.add(name, value)
                response = RestResponse(headers=res_headers, body=res_body)
                if not skip_cache:
                    self._cache[cache_key] = response
                return response

        except ClientResponseError as e:
            logger.error(f'HTTP error occurred: {e}')
            raise e
        except ClientConnectionError as e:
            logger.error(f'Connection error occurred: {e}')
            raise e
        except json.JSONDecodeError as e:
            logger.error(f'Failed to decode JSON: {e}')
            raise e
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            raise e
