import logging
import configparser
import re
import xmlschema
import importlib.resources
import sgr_schema
from collections.abc import Callable
from enum import Enum
from typing import cast

from sgr_specification.v0.product import DeviceFrame
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from sgr_commhandler.api.configuration_parameter import ConfigurationParameter, build_configuration_parameters
from sgr_commhandler.api.device_api import SGrBaseInterface
from sgr_commhandler.driver.contact.contact_interface_async import (
    SGrContactInterface,
)
from sgr_commhandler.driver.generic.generic_interface_async import (
    SGrGenericInterface,
)
from sgr_commhandler.driver.messaging.messaging_interface_async import (
    SGrMessagingInterface,
)
from sgr_commhandler.driver.modbus.modbus_interface_async import (
    SGrModbusInterface,
)
from sgr_commhandler.driver.rest.restapi_interface_async import SGrRestInterface

logger = logging.getLogger(__name__)


class SGrXmlSource(Enum):
    """Defines an EID XML source."""

    UNKNOWN = 1
    STRING = 2
    FILE = 3


class SGrPropertiesSource(Enum):
    """Defines an EID properties source."""

    UNKNOWN = 1
    DICT = 2
    FILE = 3


class SGrDeviceProtocol(Enum):
    """Defines a communication interface type."""

    MODBUS = 0
    RESTAPI = 1
    MESSAGING = 2
    CONTACT = 3
    GENERIC = 4
    UNKNOWN = 5


SGrInterfaces = (
    SGrRestInterface
    | SGrModbusInterface
    | SGrMessagingInterface
    | SGrContactInterface
    | SGrGenericInterface
)

device_builders: dict[
    SGrDeviceProtocol,
    Callable[
        [DeviceFrame],
        SGrInterfaces,
    ],
] = {
    SGrDeviceProtocol.MODBUS: lambda frame: SGrModbusInterface(
        frame, sharedRTU=True
    ),
    SGrDeviceProtocol.RESTAPI: lambda frame: SGrRestInterface(
        frame
    ),
    SGrDeviceProtocol.MESSAGING: lambda frame: SGrMessagingInterface(
        frame
    ),
    SGrDeviceProtocol.CONTACT: lambda frame: SGrContactInterface(
        frame
    ),
    SGrDeviceProtocol.GENERIC: lambda frame: SGrGenericInterface(
        frame
    ),
}


class DeviceBuilder:
    """
    Implements an SGr device builder with a fluent interface.
    """

    def __init__(self):
        """
        Constructs a new device builder.
        """

        self._eid_source: str | None = None
        self._properties_source: str | dict | None = None
        self._eid_type: SGrXmlSource = SGrXmlSource.UNKNOWN
        self._properties_type: SGrPropertiesSource = SGrPropertiesSource.UNKNOWN

    def build(self) -> SGrBaseInterface:
        """
        Constructs an SGr device instance from the builder.

        Returns
        -------
        SGrBaseInterface
            an instance of an SGr device
        """

        eid_content = self._load_eid_content()
        properties = self._load_properties()
        # parse EID - get configuration list
        frame = parse_device_frame(eid_content)
        # build final properties
        config_params = build_configuration_parameters(frame.configuration_list)
        properties = build_properties(config_params, properties)
        # parse EID - final
        eid_content = replace_variables(eid_content, properties)
        frame = parse_device_frame(eid_content)
        protocol = self._resolve_protocol(frame)
        return device_builders[protocol](frame)

    def _resolve_protocol(self, frame: DeviceFrame) -> SGrDeviceProtocol:
        if frame.interface_list is None:
            raise Exception('no device interface')
        if frame.interface_list.rest_api_interface:
            return SGrDeviceProtocol.RESTAPI
        elif frame.interface_list.modbus_interface:
            return SGrDeviceProtocol.MODBUS
        elif frame.interface_list.messaging_interface:
            return SGrDeviceProtocol.MESSAGING
        elif frame.interface_list.contact_interface:
            return SGrDeviceProtocol.CONTACT
        elif frame.interface_list.generic_interface:
            return SGrDeviceProtocol.GENERIC
        raise Exception('unsupported device interface')

    def eid_path(self, file_path: str) -> 'DeviceBuilder':
        """
        Sets the EID source to a file path.

        Parameters
        ----------
        file_path: str
            the path to the EID XML file
        
        Returns
        -------
        DeviceBuilder
            the same builder instance
        """
        
        self._eid_source = file_path
        self._eid_type = SGrXmlSource.FILE
        return self

    def eid(self, xml: str):
        """
        Sets the EID source to an XML string.

        Parameters
        ----------
        xml: str
            the EID XML content
        
        Returns
        -------
        DeviceBuilder
            the same builder instance
        """

        self._eid_source = xml
        self._eid_type = SGrXmlSource.STRING
        return self

    def properties_path(self, file_path: str):
        """
        Sets the EID properties to a file path.

        Parameters
        ----------
        file_path: str
            the path to the property file
        
        Returns
        -------
        DeviceBuilder
            the same builder instance
        """

        self._properties_type = SGrPropertiesSource.FILE
        self._properties_source = file_path
        return self

    def properties(self, properties: dict):
        """
        Sets the EID properties to a key-value map.

        Parameters
        ----------
        properties: dict
            the properties
        
        Returns
        -------
        DeviceBuilder
            the same builder instance
        """

        self._properties_type = SGrPropertiesSource.DICT
        self._properties_source = properties
        return self

    def _load_eid_content(self) -> str:
        if self._eid_source is None:
            raise Exception('No EID defined')
        content = ''
        if self._eid_type == SGrXmlSource.FILE:
            try:
                input_file = open(self._eid_source)
                content = input_file.read()
            except Exception:
                raise Exception('Invalid EID file path')
        elif self._eid_type == SGrXmlSource.STRING:
            content = self._eid_source
        return content

    def _load_properties(self) -> dict:
        if self._properties_source is None:
            logger.debug('no properties given')
            return {}
        if self._properties_type == SGrPropertiesSource.FILE:
            try:
                prop_path = str(self._properties_source)
                logger.debug(f'getting properties from file {prop_path}')
                config = configparser.RawConfigParser()
                config.optionxform = lambda option: option
                config.read(prop_path)
                properties = {}
                for section_name, section in config.items():
                    for param_name in section:
                        param_value = config.get(section_name, param_name)
                        properties[param_name] = param_value
                        logger.debug(f'found in property file: {param_name} = {param_value}')
                return properties
            except Exception as e:
                raise Exception(f'Error reading properties file {self._properties_source}: {e}')
        elif self._properties_type == SGrPropertiesSource.DICT:
            logger.debug('getting properties from dict')
            return cast(dict, self._properties_source)
        return {}


def parse_device_frame(content: str) -> DeviceFrame:
    """
    Parses EID XML content into a device frame.

    Parameters
    ----------
    content: str
        the EID XML content
    
    Returns
    -------
    DeviceFrame
        a device frame of the SGr specification
    """

    validate_schema(content)
    parser = XmlParser(context=XmlContext())
    return parser.from_string(content, DeviceFrame)


def replace_variables(content: str, parameters: dict) -> str:
    """
    Replaces parameter placeholders in EID XML content.

    Parameters
    ----------
    content: str
        the EID XML content
    parameters: dict
        the configuration parameters
    
    Returns
    -------
    str
        the updated EID XML content
    """

    for name, value in parameters.items():
        pattern = re.compile(r'{{' + str(name) + r'}}')
        content = pattern.sub(str(value), content)
        logger.debug(f'replaced parameter: {str(name)} = {str(value)}')
    return content


def build_properties(config: list[ConfigurationParameter], properties: dict) -> dict:
    """
    Builds EID configuration properties.
    Only parameters defined in the EID configuration list are kept.
    Parameters not defined in the properties are set to the default value.

    Parameters
    ----------
    config: list[ConfigurationParameter]
        the EID configuration parameters
    properties: dict
        the properties to configure
    
    Returns
    -------
    dict
        the final properties
    """

    final_properties = {}
    for config_param in config:
        prop_value = properties.get(config_param.name)
        if prop_value is not None:
            final_properties[config_param.name] = prop_value
        elif config_param.default_value is not None:
            final_properties[config_param.name] = config_param.default_value
        logger.debug(f'EID parameter: {config_param.name} = {final_properties[config_param.name]}')
    return final_properties


def validate_schema(content: str):
    """
    Validates EID XML content against the specification XML schema.

    Parameters
    ----------
    content: str
        the EID XML content
    """

    xsd_path = importlib.resources.files(sgr_schema).joinpath('SGrIncluder.xsd')
    xsd = xmlschema.XMLSchema(xsd_path)
    xsd.validate(content)
