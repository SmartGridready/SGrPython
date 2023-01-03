from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class HeaderEntry:
    header_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "headerName",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ResponseQueryType(Enum):
    JMESPATH_EXPRESSION = "JMESPathExpression"
    XPATH_EXPRESSION = "XPathExpression"
    REGULAR_EXPRESSION = "RegularExpression"


@dataclass
class HeaderList:
    header: List[HeaderEntry] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ResponseQuery:
    query_type: Optional[ResponseQueryType] = field(
        default=None,
        metadata={
            "name": "queryType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    query: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class RestServiceCall:
    request_header: Optional[HeaderList] = field(
        default=None,
        metadata={
            "name": "requestHeader",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    request_method: Optional[HttpMethod] = field(
        default=None,
        metadata={
            "name": "requestMethod",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    request_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestPath",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    request_body: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestBody",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    response_query: Optional[ResponseQuery] = field(
        default=None,
        metadata={
            "name": "responseQuery",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
