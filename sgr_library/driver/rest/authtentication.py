import json
import logging
from typing import Awaitable, Callable

import aiohttp
import jmespath
from aiohttp.client import ClientSession
from jmespath.exceptions import JMESPathError
from sgr_specification.v0.product import RestApiInterface
from sgr_specification.v0.product.rest_api_types import (
    HeaderList,
    RestApiAuthenticationMethod,
)

type Authenticator = Callable[
    [RestApiInterface, ClientSession], Awaitable[bool]
]


async def authtenicate_with_bearer_token(
    interface: RestApiInterface, session: ClientSession
) -> bool:
    try:
        description = interface.rest_api_interface_description
        if description is None:
            raise Exception("invalid")
        base_url = description.rest_api_uri
        if base_url is None:
            raise Exception("invalid")
        bearer_option = description.rest_api_bearer
        if bearer_option is None:
            raise Exception("invalid")
        rest_service = bearer_option.rest_api_service_call
        if rest_service is None:
            raise Exception("invalid")
        request_path = rest_service.request_path
        if request_path is None:
            raise Exception("invalid")

        authentication_url = f"https://{base_url}{request_path}"

        headers = {
            header_entry.header_name: header_entry.value
            for header_entry in (
                rest_service.request_header
                if rest_service.request_header
                else HeaderList()
            ).header
        }

        request_body = rest_service.request_body
        if request_body is None:
            raise Exception("illegal")

        data = json.loads(request_body)
        async with session.post(
            url=authentication_url,
            headers=headers,
            json=data,
        ) as res:
            if 200 <= res.status < 300:
                logging.info(f"Authentication successful: Status {res.status}")
                try:
                    response = await res.text()
                    token = jmespath.search("accessToken", json.loads(response))
                    if token:
                        session.headers.update(
                            {"Authorization": f"Bearer {token}"}
                        )

                        logging.info("Token retrieved successfully")
                        return True
                    else:
                        logging.warning("Token not found in the response")
                        return False
                except json.JSONDecodeError:
                    logging.error("Failed to decode JSON response")
                except JMESPathError:
                    logging.error("Failed to search JSON data using JMESPath")
            else:
                logging.warning(f"Authentication failed: Status {res.status}")
                logging.info(f"Response: {await res.text()}")

    except aiohttp.ClientError as e:
        logging.error(f"Network error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        return False


supported_authentication_methods: dict[
    RestApiAuthenticationMethod, Authenticator
] = {
    RestApiAuthenticationMethod.BEARER_SECURITY_SCHEME: authtenicate_with_bearer_token
}


async def setup_authentication(
    rest_api_interface: RestApiInterface, session: ClientSession
) -> bool:
    option = rest_api_interface.rest_api_interface_description
    if option is None:
        raise Exception("illegal")
    method = option.rest_api_authentication_method
    if method is None:
        raise Exception("illegal")
    auth_fn = supported_authentication_methods.get(method)
    if auth_fn is None:
        raise Exception("illegal")
    return await auth_fn(rest_api_interface, session)
