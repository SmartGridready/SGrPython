from typing import Callable

from aiohttp.client import ClientSession
from sgrspecification.product.rest_api_types import RestApiAuthenticationMethod

type Authenticator = Callable[[str], ClientSession]


def authtenicate_with_bearer_token(token: str) -> ClientSession:
    pass


supported_authentication_methods: dict[
    RestApiAuthenticationMethod, Authenticator
] = {
    RestApiAuthenticationMethod.BEARER_SECURITY_SCHEME: authtenicate_with_bearer_token
}
