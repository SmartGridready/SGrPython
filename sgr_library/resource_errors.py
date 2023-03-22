from enum import Enum

class ResourceError(Enum):
    """
    Default
    """
    NoError = "no_error"
    UnknownError = "unknown_error"

    """
    XML
    """
    XMLParsingError = "xml_parsing_error"
    XMLMissingValueError = "xml_missing_value_error"

    """
    Connection
    """
    ConnectionError = "connection_error"
    CredentialError = "credential_error"
    RequestCreationError = "request_creation_error"
    AuthenticationError = "authentication_error"
    