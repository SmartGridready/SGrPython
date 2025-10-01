import base64
import json
import logging
import re
from typing import Any, Awaitable, Callable, TypeAlias

import aiohttp
import jmespath
from aiohttp.client import ClientSession
from jmespath.exceptions import JMESPathError
from multidict import CIMultiDict
from sgr_specification.v0.generic.base_types import ResponseQueryType
from sgr_specification.v0.product import RestApiInterface
from sgr_specification.v0.product.rest_api_types import (
    RestApiAuthenticationMethod,
)
from sgr_commhandler.utils import jmespath_mapping
from sgr_commhandler.driver.rest.request import (
    RestResponse,
    build_rest_request
)

logger = logging.getLogger(__name__)

Authenticator: TypeAlias = Callable[
    [RestApiInterface, ClientSession], Awaitable[bool]
]


async def authenticate_not(
    interface: RestApiInterface, session: ClientSession
) -> bool:
    """
    Skips authentication.

    Parameters
    ----------
    interface : RestApiInterface
        the device interface
    session : ClientSession
        the REST client session
    
    Returns
    -------
    bool
        True if authenticated, False otherwise
    """

    return True


async def authenticate_with_bearer_token(
    interface: RestApiInterface, session: ClientSession
) -> bool:
    """
    Authenticates using Bearer token (JWT).

    Parameters
    ----------
    interface : RestApiInterface
        the device interface
    session : ClientSession
        the REST client session
    
    Returns
    -------
    bool
        True if authenticated, False otherwise
    """

    try:
        description = interface.rest_api_interface_description
        if description is None:
            raise Exception("no interface description")
        base_url = description.rest_api_uri
        if base_url is None:
            raise Exception("no base URL")
        bearer_option = description.rest_api_bearer
        if bearer_option is None:
            raise Exception("no Bearer option")
        service_call = bearer_option.rest_api_service_call
        if service_call is None:
            raise Exception("no REST service call for authentication")
        request_path = service_call.request_path
        if request_path is None:
            raise Exception("no request path")

        authentication_url = f"{base_url}{request_path}"
        logger.debug(f'auth URL = {authentication_url}')

        request = build_rest_request(service_call, base_url, {})

        async with session.request(
                request.method,
                request.url,
                headers=request.headers,
                params=request.query_parameters,
                data=request.body
            ) as req:
                if 200 <= req.status < 300:
                    logger.info(f"Bearer authentication successful: Status {req.status}")
                    try:
                        res_body = await req.text()
                        res_headers = CIMultiDict()
                        for name, value in req.headers.items():
                            res_headers.add(name, value)

                        response = RestResponse(headers=res_headers, body=res_body)

                        # extract token from response body
                        if response.body is not None:
                            token: Any
                            if (
                                service_call.response_query
                                and service_call.response_query.query_type == ResponseQueryType.JMESPATH_EXPRESSION
                            ):
                                # JMESPath expression
                                query_expression = service_call.response_query.query if service_call.response_query.query else ''
                                token = jmespath.search(query_expression, json.loads(response.body))
                            elif (
                                service_call.response_query
                                and service_call.response_query.query_type == ResponseQueryType.JMESPATH_MAPPING
                            ):
                                # JMESPath mappings
                                mappings = service_call.response_query.jmes_path_mappings.mapping if service_call.response_query.jmes_path_mappings else []
                                token = jmespath_mapping.map_json_response(response.body, mappings)
                            elif (
                                service_call.response_query
                                and service_call.response_query.query_type == ResponseQueryType.REGULAR_EXPRESSION
                            ):
                                # regex
                                query_expression = service_call.response_query.query if service_call.response_query.query else ''
                                query_match = re.match(query_expression, response.body)
                                token = query_match.group() if query_match is not None else None
                            else:
                                # plaintext
                                token = response.body

                            if token is not None:
                                # update authorization header in active session
                                session.headers.update(
                                    {"Authorization": f"Bearer {token}"}
                                )
                                logger.info("Bearer token retrieved successfully")
                                return True

                        logger.warning("Bearer token not found in the response")
                        return False
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON response")
                    except JMESPathError:
                        logger.error("Failed to search JSON data using JMESPath")
                else:
                    logger.warning(f"Bearer authentication failed: Status {req.status}")
                    logger.debug(f"Response: {await req.text()}")
    except aiohttp.ClientError as e:
        logger.error(f"Network error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        return False


async def authenticate_with_basic_auth(
    interface: RestApiInterface, session: ClientSession
) -> bool:
    """
    Authenticates using Basic Authentication.

    Parameters
    ----------
    interface : RestApiInterface
        the device interface
    session : ClientSession
        the REST client session
    
    Returns
    -------
    bool
        True if authenticated, False otherwise
    """

    description = interface.rest_api_interface_description
    if description is None:
        raise Exception("no interface description")
    basic_option = description.rest_api_basic
    if basic_option is None:
        raise Exception("no Basic option")
    username = basic_option.rest_basic_username if basic_option.rest_basic_username is not None else ''
    password = basic_option.rest_basic_password if basic_option.rest_basic_password is not None else ''

    # cannot use aiohttp.BasicAuth here, must set headers
    credentials = f'{username}:{password}'
    session.headers.update(
        {"Authorization": f"Basic {base64.urlsafe_b64encode(bytes(credentials, 'utf-8')).decode('utf-8')}"}
    )

    return True


supported_authentication_methods: dict[
    RestApiAuthenticationMethod, Authenticator
] = {
    RestApiAuthenticationMethod.NO_SECURITY_SCHEME: authenticate_not,
    RestApiAuthenticationMethod.BEARER_SECURITY_SCHEME: authenticate_with_bearer_token,
    RestApiAuthenticationMethod.BASIC_SECURITY_SCHEME: authenticate_with_basic_auth
}


async def setup_authentication(
    rest_api_interface: RestApiInterface, session: ClientSession
) -> bool:
    """
    Performs authentication asynchronously, depending on the configured method.

    Parameters
    ----------
    interface : RestApiInterface
        the device interface
    session : ClientSession
        the REST client session
    
    Returns
    -------
    bool
        True if authenticated, False otherwise
    """
    descr = rest_api_interface.rest_api_interface_description
    if descr is None:
        raise Exception("no REST interface description")
    method = descr.rest_api_authentication_method
    if method is None:
        raise Exception("no authentication method")
    auth_fn = supported_authentication_methods.get(method)
    if auth_fn is None:
        raise Exception("unsupported authentication method")
    return await auth_fn(rest_api_interface, session)
