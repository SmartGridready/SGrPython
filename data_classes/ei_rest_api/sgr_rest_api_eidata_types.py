from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from data_classes.ei_gen_tcp_ip.sgr_tsp_srv_tcp_ip import (
    TPipV4GenAddrType,
    TPipV6GenAddrType,
)
from data_classes.generic.sgr_gen_data_point_definition import SgrDataPointDescriptionType
from data_classes.generic.sgr_gen_functional_profile_definition import SgrProfileDescriptionType
from data_classes.generic.sgr_gen_type_definitions import SgrAttr4GenericType

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
class SgrrestApibearerType:
    class Meta:
        name = "SGRrestAPIBearerType"

    rest_apiend_point: Optional[str] = field(
        default=None,
        metadata={
            "name": "restAPIEndPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_apijmespath: Optional[str] = field(
        default=None,
        metadata={
            "name": "restAPIJMESPath",
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
class SgrRestApidataPointDescriptionType:
    class Meta:
        name = "SGrRestAPIDataPointDescriptionType"

    rest_apiend_point: Optional[str] = field(
        default=None,
        metadata={
            "name": "restAPIEndPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    rest_apijmespath: Optional[str] = field(
        default=None,
        metadata={
            "name": "restAPIJMESPath",
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


@dataclass
class SgrRestApidataPointsFrameType:
    """RPT Root Point for stand alone RestAPI Functional Profile description.

    It includes the embedded generic Porfile decription
    """
    class Meta:
        name = "SGrRestAPIDataPointsFrameType"

    data_point: List[SgrDataPointDescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "dataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    rest_apidata_point: List[SgrRestApidataPointDescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "restAPIDataPoint",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_apiattr: List[SgrAttr4RestApitype] = field(
        default_factory=list,
        metadata={
            "name": "restAPIAttr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrRestApiprofilesFrameType:
    class Meta:
        name = "SGrRestAPIProfilesFrameType"

    functional_profile: Optional[SgrProfileDescriptionType] = field(
        default=None,
        metadata={
            "name": "functionalProfile",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    gen_attribute: List[SgrAttr4GenericType] = field(
        default_factory=list,
        metadata={
            "name": "genAttribute",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rest_apiattr: List[SgrAttr4RestApitype] = field(
        default_factory=list,
        metadata={
            "name": "restAPIAttr",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_list_element: List[SgrRestApidataPointsFrameType] = field(
        default_factory=list,
        metadata={
            "name": "dpListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
