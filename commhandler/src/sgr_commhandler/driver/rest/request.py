from typing import Optional
from urllib.parse import urlencode
from multidict import CIMultiDict
from sgr_specification.v0.product import (
    HeaderList,
    HttpMethod,
)
from sgr_specification.v0.product.rest_api_types import (
    ParameterList,
    RestApiServiceCall
)
from sgr_commhandler.utils import template


class RestResponse:
    """
    Implements a REST response.
    """

    def __init__(self, headers: CIMultiDict[str] = CIMultiDict(), body: Optional[str] = None):
        self.headers = headers
        self.body = body


class RestRequest:
    """
    Implements a REST request.
    """

    def __init__(
        self,
        method: str,
        url: str,
        headers: CIMultiDict[str] = CIMultiDict(),
        query_parameters: CIMultiDict[str] = CIMultiDict(),
        form_parameters: CIMultiDict[str] = CIMultiDict(),
        body: Optional[str] = None,
    ):
        self.method = method
        self.url = url
        self.headers = headers
        self.query_parameters = query_parameters
        self.form_parameters = form_parameters
        self.body = body


def build_rest_request(call_spec: RestApiServiceCall, base_url: str, substitutions: dict[str, str]) -> RestRequest:
    """
    Builds a REST request.

    Parameters
    ----------
    call_spec : RestApiServiceCall
        the REST call specification
    base_url : str
        the base URL of the HTTP request
    substitutions : dict[str, str]
        parameter substitutions

    Returns
    -------
    RestRequest
        the created request
    """

    # copy from DP spec.
    method = call_spec.request_method if call_spec.request_method else HttpMethod.GET
    req_path = str(call_spec.request_path) if call_spec.request_path else ''
    headers = call_spec.request_header if call_spec.request_header else HeaderList()
    query = call_spec.request_query if call_spec.request_query else ParameterList()
    form = call_spec.request_form if call_spec.request_form else ParameterList()
    body=str(call_spec.request_body) if call_spec.request_body else None

    # All headers into dictionary, with substitution
    request_headers: CIMultiDict[str] = CIMultiDict()
    for header_entry in headers.header:
        if header_entry.header_name and header_entry.value:
            request_headers.add(header_entry.header_name, template.substitute(header_entry.value, substitutions))

    # All query parameters into dictionary, with substitution
    query_parameters: CIMultiDict[str] = CIMultiDict()
    for param_entry in query.parameter:
        if param_entry.name and param_entry.value:
            query_parameters.add(param_entry.name, template.substitute(param_entry.value, substitutions))

    # All form parameters into dictionary, with substitution
    form_parameters: CIMultiDict[str] = CIMultiDict()
    for param_entry in form.parameter:
        if param_entry.name and param_entry.value:
            form_parameters.add(param_entry.name, template.substitute(param_entry.value, substitutions))

    # request path, with substitution
    request_path = template.substitute(req_path, substitutions)

    # request body, with substitution
    request_body: Optional[str] = template.substitute(body, substitutions) if body is not None else None

    # override body when form parameters are set
    if len(form_parameters) > 0:
        request_body = urlencode(form_parameters)
        request_headers['Content-Type'] = (
            'application/x-www-form-urlencoded'
        )

    base_url = f'{base_url}{request_path}'

    return RestRequest(
        method.value,
        base_url,
        request_headers,
        query_parameters,
        form_parameters,
        request_body
    )
