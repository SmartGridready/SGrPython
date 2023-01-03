from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from data_classes.ei_rest_api.sgr_rest_api_rest_service_call import RestServiceCall
from data_classes.generic.sgr_tsp_srv_tcp_ip import (
    TPipV4GenAddrType,
    TPipV6GenAddrType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrRestBasicType:
    class Meta:
        name = " SGrRestBasicType"

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


@dataclass
class SgrAttr4RestApitype:
    class Meta:
        name = "SGrAttr4RestAPIType"

    place_holder4future_extensions: Optional[str] = field(
        default=None,
        metadata={
            "name": "placeHolder4futureExtensions",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class SgrRestApiauthenticationEnumMethodType(Enum):
    NO_SECURITY_SCHEME = "NoSecurityScheme"
    BEARER_SECURITY_SCHEME = "BearerSecurityScheme"
    APIKEY_SECURITY_SCHEME = "APIKeySecurityScheme"
    BASIC_SECURITY_SCHEME = "BasicSecurityScheme"
    DIGEST_SECURITY_SCHEME = "DigestSecurityScheme"
    PSKSECURITY_SCHEME = "PSKSecurityScheme"
    OAUTH1_SECURITY_SCHEME = "OAuth1SecurityScheme"
    OAUTH2_SECURITY_SCHEME = "OAuth2SecurityScheme"
    HAWK_SECURITY_SCHEME = "HawkSecurityScheme"
    AWS_SIGNATURE_SECURITY_SCHEME = "AWS_SignatureSecurityScheme"
    NTLMSECURITY_SCHEME = "NTLMSecurityScheme"
    AKAMAI_EDGE_GRID_SECURITY_SCHEME = "AkamaiEdgeGridSecurityScheme"


class SgrRestApiinterfaceSelectiontype(Enum):
    TRSP_SRV_REST_TCPV4 = "trspSrvRestTCPV4"
    TRSP_SRV_REST_TCPV6 = "trspSrvRestTCPV6"
    TRSP_SRV_REST_URI = "trspSrvRestURI"


class SgrRestApidataTypeType(Enum):
    NULL = "null"
    JSON_NUMBER = "JSON_number"
    JSON_STRING = "JSON_string"
    JSON_BOOLEAN = "JSON_boolean"
    JSON_OBJECT = "JSON_object"
    JSON_ARRAY = "JSON_array"


@dataclass
class SgrrestApibearerType:
    class Meta:
        name = "SGRrestAPIBearerType"

    service_call: Optional[RestServiceCall] = field(
        default=None,
        metadata={
            "name": "serviceCall",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class SgrRestApidataPointDescriptionType:
    class Meta:
        name = "SGrRestAPIDataPointDescriptionType"

    rest_service_call: Optional[RestServiceCall] = field(
        default=None,
        metadata={
            "name": "restServiceCall",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    data_type: Optional[SgrRestApidataTypeType] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Attribute",
        }
    )


@dataclass
class SgrRestApiinterfaceDescriptionType:
    class Meta:
        name = "SGrRestAPIInterfaceDescriptionType"

    rest_apiinterface_selection: Optional[SgrRestApiinterfaceSelectiontype] = field(
        default=None,
        metadata={
            "name": "restAPIInterfaceSelection",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    trsp_srv_rest_tcpv4out_of_box: Optional[TPipV4GenAddrType] = field(
        default=None,
        metadata={
            "name": "trspSrvRestTCPV4outOfBox",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    trsp_srv_rest_tcpv6out_of_box: Optional[TPipV6GenAddrType] = field(
        default=None,
        metadata={
            "name": "trspSrvRestTCPV6outOfBox",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    trsp_srv_rest_uriout_of_box: Optional[str] = field(
        default=None,
        metadata={
            "name": "trspSrvRestURIoutOfBox",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_apiauthentication_method: Optional[SgrRestApiauthenticationEnumMethodType] = field(
        default=None,
        metadata={
            "name": "restAPIAuthenticationMethod",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_apibearer: Optional[SgrrestApibearerType] = field(
        default=None,
        metadata={
            "name": "restAPIBearer",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_apibasic: Optional[str] = field(
        default=None,
        metadata={
            "name": "restAPIBasic",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
