import json
import logging
from typing import Awaitable, Callable, TypeAlias

import aiohttp
import jmespath
from aiohttp.client import ClientSession
from jmespath.exceptions import JMESPathError
from sgr_specification.v0.product import RestApiInterface
from sgr_specification.v0.product.rest_api_types import (
    HeaderList,
    RestApiAuthenticationMethod,
)

logger = logging.getLogger(__name__)

Authenticator: TypeAlias = Callable[
    [RestApiInterface, ClientSession], Awaitable[bool]
]


async def authenticate_not(
    interface: RestApiInterface, session: ClientSession
) -> bool:
    # skip authentication
    return True


async def authenticate_with_bearer_token(
    interface: RestApiInterface, session: ClientSession
) -> bool:
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
        logger.debug("auth URL = " + authentication_url)

        headers = {
            header_entry.header_name: header_entry.value
            for header_entry in (
                service_call.request_header
                if service_call.request_header
                else HeaderList()
            ).header
        }

        request_body = service_call.request_body
        if request_body is None:
            raise Exception("no request body")

        data = json.loads(request_body)
        async with session.post(
            url=authentication_url,
            headers=headers,
            json=data,
        ) as res:
            if 200 <= res.status < 300:
                logger.info(f"Authentication successful: Status {res.status}")
                try:
                    response = await res.text()
                    token = jmespath.search("accessToken", json.loads(response))
                    if token:
                        session.headers.update(
                            {"Authorization": f"Bearer {token}"}
                        )

                        logger.info("Token retrieved successfully")
                        return True
                    else:
                        logger.warning("Token not found in the response")
                        return False
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON response")
                except JMESPathError:
                    logger.error("Failed to search JSON data using JMESPath")
            else:
                logger.warning(f"Authentication failed: Status {res.status}")
                logger.info(f"Response: {await res.text()}")

    except aiohttp.ClientError as e:
        logger.error(f"Network error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        return False


supported_authentication_methods: dict[
    RestApiAuthenticationMethod, Authenticator
] = {
    RestApiAuthenticationMethod.NO_SECURITY_SCHEME: authenticate_not,
    RestApiAuthenticationMethod.BEARER_SECURITY_SCHEME: authenticate_with_bearer_token,
}


async def setup_authentication(
    rest_api_interface: RestApiInterface, session: ClientSession
) -> bool:
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
