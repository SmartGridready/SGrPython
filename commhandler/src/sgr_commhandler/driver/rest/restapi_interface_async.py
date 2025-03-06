import json
import logging
import ssl
from io import UnsupportedOperation
from typing import Any, Callable, Optional
from urllib.parse import urlencode

import aiohttp
import certifi
import jmespath
from aiohttp import ClientConnectionError, ClientResponseError
from cachetools import TTLCache
from sgr_specification.v0.generic import DataDirectionProduct
from sgr_specification.v0.generic.base_types import ResponseQueryType
from sgr_specification.v0.product import (
    DeviceFrame,
    HeaderEntry,
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

from sgr_commhandler.api import (
    DataPoint,
    DataPointProtocol,
    FunctionalProfile,
    SGrBaseInterface,
)
from sgr_commhandler.driver.rest.authentication import setup_authentication
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def build_rest_data_point(
    data_point: RestApiDataPointSpec,
    function_profile: RestApiFunctionalProfileSpec,
    interface: 'SGrRestInterface',
) -> DataPoint:
    protocol = RestDataPoint(data_point, function_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


class RestResponse:
    def __init__(self, headers: HeaderList, body: Optional[str] = None):
        self.headers = headers
        self.body = body


class RestRequest:
    def __init__(
        self,
        method: HttpMethod,
        url: str,
        headers: HeaderList,
        query_parameters: ParameterList = ParameterList(),
        form_parameters: ParameterList = ParameterList(),
        body: Optional[str] = None,
    ):
        self.method = method
        self.url = url
        self.headers = headers
        self.query_parameters = query_parameters
        self.form_parameters = form_parameters
        self.body = body


class RestDataPoint(DataPointProtocol):
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

    async def get_val(self, skip_cache: bool = False):
        if not self._read_call:
            raise Exception('No read call')

        # TODO das scheint auch noch falsch muss ein reqeust jeweils alle parameter haben?
        request = RestRequest(
            self._read_call.request_method,
            f'{self._interface.base_url}{self._read_call.request_path}',
            self._read_call.request_header,
            self._read_call.request_query,
            self._read_call.request_form,
            self._read_call.request_body,
        )
        response = await self._interface.execute_request(request, skip_cache)
        if not response.body:
            return None
        if (
            self._read_call.response_query
            and self._read_call.response_query.query_type
            == ResponseQueryType.JMESPATH_EXPRESSION
        ):
            query_expression = self._read_call.response_query.query
            return jmespath.search(query_expression, json.loads(response.body))
        ret_value = response.body

        # convert to DP units
        if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.unit_conversion_multiplicator
            and self._dp_spec.data_point.unit_conversion_multiplicator != 1.0
        ):
            ret_value = (
                float(ret_value)
                * self._dp_spec.data_point.unit_conversion_multiplicator
            )

        return ret_value

    async def set_val(self, value: Any):
        if not self._write_call:
            raise Exception('No write call')

        # convert to device units
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.unit_conversion_multiplicator
            and self._dp_spec.data_point.unit_conversion_multiplicator != 1.0
        ):
            value = (
                float(value)
                / self._dp_spec.data_point.unit_conversion_multiplicator
            )

        # TODO auch hier scheint alles no ein bisschen fehlerhaft
        # replace {{value}} placeholder
        request = RestRequest(
            self._write_call.request_method,
            f'{self._interface.base_url}{self._write_call.request_path}',
            self._write_call.request_header,
            self._write_call.request_query,
            self._write_call.request_form,
            body=str(self._write_call.request_body).replace(
                '{{value}}', str(value)
            )
            if self._write_call.request_body
            else None,
        )
        # TODO use response body
        await self._interface.execute_request(request, skip_cache=True)

    def direction(self) -> DataDirectionProduct:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction

    def subscribe(self, fn: Callable[[Any], None]):
        raise UnsupportedOperation(
            'subscribe is no available for rest datapoint'
        )

    def unsubscribe(self):
        raise UnsupportedOperation(
            'unsubscribe is no available for rest datapoint'
        )


class RestFunctionalProfile(FunctionalProfile):
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


class SGrRestInterface(SGrBaseInterface):
    """
    SmartGridready External Interface Class for Rest API
    """

    def __init__(
        self, frame: DeviceFrame
    ):
        self._inititalize_device(frame)
        self._session = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._connector = aiohttp.TCPConnector(ssl=self._ssl_context)
        self._cache = TTLCache(maxsize=100, ttl=5)

        if (
            self.frame.interface_list
            and self.frame.interface_list
            and self.frame.interface_list.rest_api_interface
        ):
            self._raw_interface = self.frame.interface_list.rest_api_interface
        else:
            raise Exception('No REST interface')
        desc = self._raw_interface.rest_api_interface_description
        if desc is None:
            raise Exception('No REST interface description')
        self.base_url = desc.rest_api_uri
        if self.base_url is None:
            raise Exception('Invalid base URL')

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [RestFunctionalProfile(profile, self) for profile in raw_fps]
        self.function_profiles = {fp.name(): fp for fp in fps}

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
            # All headers into dictionary
            request_headers = {
                header_entry.header_name: header_entry.value
                for header_entry in request.headers.header
            }

            # All query parameters into dictionary
            query_parameters = {
                param_entry.name: param_entry.value
                for param_entry in request.query_parameters.parameter
            }

            request_body: Optional[str] = request.body

            # All form parameters into dictionary
            form_parameters = {
                param_entry.name: param_entry.value
                for param_entry in request.form_parameters.parameter
            }
            # override body
            if len(form_parameters) > 0:
                request_body = urlencode(form_parameters)
                request_headers['Content-Type'] = (
                    'application/x-www-form-urlencoded'
                )

            cache_key = (frozenset(request_headers), request.url)
            if not skip_cache and cache_key in self._cache:
                return self._cache[cache_key]

            async with self._session.request(
                request.method.value,
                request.url,
                headers=request_headers,
                params=query_parameters,
                data=request_body,
            ) as req:
                req.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                logger.info(f'execute_request status: {req.status}')
                res_body = await req.text()

                sgr_headers = []
                for name, value in req.headers.items():
                    sgr_headers.append(
                        HeaderEntry(header_name=name, value=value)
                    )
                header_list = HeaderList(header=sgr_headers)
                response = RestResponse(headers=header_list, body=res_body)
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
