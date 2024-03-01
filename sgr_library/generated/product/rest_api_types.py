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
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class JmespathMappingRecord:
    class Meta:
        name = "JMESPathMappingRecord"

    from_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "from",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    to: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


class ResponseQueryType(Enum):
    JMESPATH_EXPRESSION = "JMESPathExpression"
    XPATH_EXPRESSION = "XPathExpression"
    REGULAR_EXPRESSION = "RegularExpression"
    JMESPATH_MAPPING = "JMESPathMapping"


class RestApiAuthenticationMethod(Enum):
    NO_SECURITY_SCHEME = "NoSecurityScheme"
    BEARER_SECURITY_SCHEME = "BearerSecurityScheme"
    API_KEY_SECURITY_SCHEME = "ApiKeySecurityScheme"
    BASIC_SECURITY_SCHEME = "BasicSecurityScheme"
    DIGEST_SECURITY_SCHEME = "DigestSecurityScheme"
    PSK_SECURITY_SCHEME = "PskSecurityScheme"
    OAUTH1_SECURITY_SCHEME = "OAuth1SecurityScheme"
    OAUTH2_SECURITY_SCHEME = "OAuth2SecurityScheme"
    HAWK_SECURITY_SCHEME = "HawkSecurityScheme"
    AWS_SIGNATURE_SECURITY_SCHEME = "AwsSignatureSecurityScheme"
    NTLM_SECURITY_SCHEME = "NtlmSecurityScheme"
    AKAMAI_EDGE_GRID_SECURITY_SCHEME = "AkamaiEdgeGridSecurityScheme"


@dataclass
class RestApiBasic:
    rest_basic_username: Optional[str] = field(
        default=None,
        metadata={
            "name": "restBasicUsername",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_basic_password: Optional[str] = field(
        default=None,
        metadata={
            "name": "restBasicPassword",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class RestApiDataType(Enum):
    """
    Rest api specific data types.
    """
    NULL = "null"
    JSON_NUMBER = "JSON_number"
    JSON_STRING = "JSON_string"
    JSON_BOOLEAN = "JSON_boolean"
    JSON_OBJECT = "JSON_object"
    JSON_ARRAY = "JSON_array"


class RestApiInterfaceSelection(Enum):
    """
    Type of Rest Api interface.
    """
    TCPV4 = "TCPV4"
    TCPV6 = "TCPV6"
    URI = "URI"


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
class JmespathMapping:
    class Meta:
        name = "JMESPathMapping"

    mapping: List[JmespathMappingRecord] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
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
        }
    )
    jmes_path_mappings: Optional[JmespathMapping] = field(
        default=None,
        metadata={
            "name": "jmesPathMappings",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class RestApiServiceCall:
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


@dataclass
class RestApiBearer:
    rest_api_service_call: Optional[RestApiServiceCall] = field(
        default=None,
        metadata={
            "name": "restApiServiceCall",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class RestApiDataPointConfiguration:
    """
    Detailed configuration for Rest api data point.
    """
    data_type: Optional[RestApiDataType] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_api_service_call: Optional[RestApiServiceCall] = field(
        default=None,
        metadata={
            "name": "restApiServiceCall",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class RestApiInterfaceDescription:
    """
    Modbus interface properties.
    """
    rest_api_interface_selection: Optional[RestApiInterfaceSelection] = field(
        default=None,
        metadata={
            "name": "restApiInterfaceSelection",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_api_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "restApiUri",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_api_authentication_method: Optional[RestApiAuthenticationMethod] = field(
        default=None,
        metadata={
            "name": "restApiAuthenticationMethod",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_api_bearer: Optional[RestApiBearer] = field(
        default=None,
        metadata={
            "name": "restApiBearer",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_api_basic: Optional[RestApiBasic] = field(
        default=None,
        metadata={
            "name": "restApiBasic",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
