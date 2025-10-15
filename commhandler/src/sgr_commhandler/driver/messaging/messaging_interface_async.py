import asyncio
import json
import logging
import re
import jmespath
from collections.abc import Callable
from typing import Any, NoReturn, Optional

from sgr_specification.v0.generic import DataDirectionProduct, Units, ResponseQueryType
from sgr_specification.v0.product import (
    DeviceFrame,
    MessagingDataPoint as MessagingDataPointSpec,
    MessagingFunctionalProfile as MessagingFunctionalProfileSpec,
    MessagingInterfaceDescription,
    MessagingPlatformType,
    InMessage,
    OutMessage
)

from sgr_commhandler.api.dynamic_parameter import build_dynamic_parameter_substitutions, build_dynamic_parameters
from sgr_commhandler.utils import jmespath_mapping, template
from sgr_commhandler.driver.messaging.messaging_filter import (
    MessagingFilter,
    get_messaging_filter
)
from sgr_commhandler.driver.messaging.messaging_client_async import SGrMessagingClient, SGrMqttClient
from sgr_commhandler.api.data_point_api import (
    DataPoint,
    DataPointProtocol,
)
from sgr_commhandler.api.functional_profile_api import (
    FunctionalProfile
)
from sgr_commhandler.api.device_api import (
    SGrBaseInterface
)
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def build_messaging_data_point(
    data_point: MessagingDataPointSpec,
    functional_profile: MessagingFunctionalProfileSpec,
    interface: 'SGrMessagingInterface',
) -> DataPoint:
    """
    Builds a data point of a messaging interface.
    """
    protocol = MessagingDataPoint(data_point, functional_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


def get_messaging_client(name: str, desc: MessagingInterfaceDescription) -> SGrMessagingClient:
    """
    Builds a messaging client from the interface specification.
    """
    if desc.platform is not None and desc.platform == MessagingPlatformType.MQTT5:

        brokers = desc.message_broker_list.message_broker_list_element if (
            desc.message_broker_list
            and desc.message_broker_list.message_broker_list_element
        ) else list()
        if len(brokers) == 0:
            raise Exception('no message brokers')

        # basic authentication supported
        credentials = (
            str(desc.message_broker_authentication.basic_authentication.username),
            str(desc.message_broker_authentication.basic_authentication.password)
        ) if (
            desc.message_broker_authentication
            and desc.message_broker_authentication.basic_authentication
        ) else None

        # verify certificate option not supported!
        return SGrMqttClient(
            str(brokers[0].host),
            int(str(brokers[0].port)),
            name,
            credentials=credentials
        )
    raise Exception('no supported platform')


class MessagingDataPoint(DataPointProtocol[MessagingDataPointSpec]):
    """
    Implements a data point of a messaging interface.
    """

    def __init__(
        self,
        dp_spec: MessagingDataPointSpec,
        fp_spec: MessagingFunctionalProfileSpec,
        interface: 'SGrMessagingInterface',
    ):
        self._dp_spec = dp_spec
        self._fp_spec = fp_spec

        dp_config = self._dp_spec.messaging_data_point_configuration
        if not dp_config:
            raise Exception('Messaging data point configuration missing')

        self._dynamic_parameters = build_dynamic_parameters(
            self._dp_spec.data_point.parameter_list
            if self._dp_spec.data_point
            else None
        )

        self._fp_name = ''
        if (
            fp_spec.functional_profile is not None
            and fp_spec.functional_profile.functional_profile_name is not None
        ):
            self._fp_name = fp_spec.functional_profile.functional_profile_name

        self._dp_name = ''
        if (
            dp_spec.data_point is not None
            and dp_spec.data_point.data_point_name is not None
        ):
            self._dp_name = dp_spec.data_point.data_point_name

        self._in_cmd: Optional[InMessage] = None
        self._read_cmd: Optional[OutMessage] = None
        self._write_cmd: Optional[OutMessage] = None
        self._in_filter: Optional[MessagingFilter] = None
        self._read_response_event: Optional[asyncio.Event] = None
        if self._dp_spec.messaging_data_point_configuration:
            if self._dp_spec.messaging_data_point_configuration.in_message:
                self._in_cmd = self._dp_spec.messaging_data_point_configuration.in_message
                if self._in_cmd.filter:
                    self._in_filter = get_messaging_filter(self._in_cmd.filter)
            if self._dp_spec.messaging_data_point_configuration.read_cmd_message:
                self._read_cmd = self._dp_spec.messaging_data_point_configuration.read_cmd_message
                self._read_response_event = asyncio.Event()
            if self._dp_spec.messaging_data_point_configuration.write_cmd_message:
                self._write_cmd = self._dp_spec.messaging_data_point_configuration.write_cmd_message

        self._cached_value: Any = None
        self._handle_message: Optional[Callable[[DataPointProtocol, Any], NoReturn]] = None
        self._interface = interface
        if self._in_cmd and self._in_cmd.topic:
            self._interface.data_point_handler((self._fp_name, self._dp_name, self._in_cmd.topic, self._on_message, self._in_filter))  # type: ignore

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    def get_specification(self) -> MessagingDataPointSpec:
        return self._dp_spec

    async def get_val(self, parameters: Optional[dict[str, str]] = None, skip_cache: bool = False) -> Any:
        if not self._read_cmd:
            # passive reading only
            logger.debug('passive reading')
            return self._cached_value

        if not skip_cache and self._cached_value:
            logger.debug('reading cached value')
            return self._cached_value

        msg_body = self._read_cmd.template or ''
        substitutions = build_dynamic_parameter_substitutions(self._dynamic_parameters, parameters)
        msg_body = template.substitute(msg_body, substitutions)

        logger.debug('active reading...')
        await self._interface.write_message(str(self._read_cmd.topic), msg_body)
        if self._read_response_event:
            await self._read_response_event.wait()

        logger.debug('finished active reading...')
        return self._cached_value

    async def set_val(self, value: Any):
        if not self._write_cmd or not self._write_cmd.topic:
            raise Exception('No write topic')

        # convert to device units
        unit_conv_factor = self._dp_spec.data_point.unit_conversion_multiplicator if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.unit_conversion_multiplicator
        ) else 1.0
        if unit_conv_factor != 1.0:
            value = float(value) / unit_conv_factor

        # apply value mappings
        value = str(value)
        if self._write_cmd.value_mapping:
            mappings = self._write_cmd.value_mapping.mapping
            for m in mappings:
                if m.generic_value == value:
                    value = m.device_value
                    break
        # add value to substitutions
        substitutions = {
            'value': value
        }
        value = template.substitute(value, substitutions)
        await self._interface.write_message(self._write_cmd.topic, value)
        self._cached_value = value

    def direction(self) -> DataDirectionProduct:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction

    def unit(self) -> Units:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.unit is None
        ):
            return Units.NONE
        return self._dp_spec.data_point.unit

    def can_subscribe(self) -> bool:
        return True

    def subscribe(self, fn: Callable[[DataPointProtocol, Any], NoReturn]):  # type: ignore
        self._handle_message = fn

    def unsubscribe(self):  # type: ignore
        self._handle_message = None

    def _on_message(self, payload: Any):  # type: ignore
        ret_value: Any
        if (
            self._in_cmd
            and self._in_cmd.response_query
            and self._in_cmd.response_query.query_type == ResponseQueryType.JMESPATH_EXPRESSION
        ):
            # JMESPath expression
            query_expression = self._in_cmd.response_query.query if self._in_cmd.response_query.query else ''
            ret_value = jmespath.search(query_expression, json.loads(payload))
        elif (
            self._in_cmd
            and self._in_cmd.response_query
            and self._in_cmd.response_query.query_type == ResponseQueryType.JMESPATH_MAPPING
        ):
            # JMESPath mappings
            mappings = self._in_cmd.response_query.jmes_path_mappings.mapping if self._in_cmd.response_query.jmes_path_mappings else []
            ret_value = jmespath_mapping.map_json_response(str(payload), mappings)
        elif (
            self._in_cmd
            and self._in_cmd.response_query
            and self._in_cmd.response_query.query_type == ResponseQueryType.REGULAR_EXPRESSION
        ):
            # regex
            query_expression = self._in_cmd.response_query.query if self._in_cmd.response_query.query else ''
            query_match = re.match(query_expression, str(payload))
            ret_value = query_match.group() if query_match is not None else str(payload)
        else:
            # plain response
            ret_value = str(payload)

            # apply value mappings
            if self._in_cmd and self._in_cmd.value_mapping:
                mappings = self._in_cmd.value_mapping.mapping
                for m in mappings:
                    if m.device_value == ret_value:
                        ret_value = str(m.generic_value)
                        break

            # convert to DP units
            if (
                self._dp_spec.data_point
                and self._dp_spec.data_point.unit_conversion_multiplicator
                and self._dp_spec.data_point.unit_conversion_multiplicator != 1.0
            ):
                ret_value = (
                    float(ret_value)
                    * self._dp_spec.data_point.unit_conversion_multiplicator
                )

        # update data point value
        self._cached_value = ret_value
        if self._read_response_event:
            self._read_response_event.set()
        if self._handle_message is not None:
            self._handle_message(self, ret_value)


class MessagingFunctionalProfile(FunctionalProfile[MessagingFunctionalProfileSpec]):
    """
    Implements a functional profile of a messaging interface.
    """

    def __init__(
        self,
        fp_spec: MessagingFunctionalProfileSpec,
        interface: 'SGrMessagingInterface',
    ):
        self._fp_spec = fp_spec
        self._interface = interface

        raw_dps = []
        if (
            self._fp_spec.data_point_list
            and self._fp_spec.data_point_list.data_point_list_element
        ):
            raw_dps = self._fp_spec.data_point_list.data_point_list_element

        dps = [
            build_messaging_data_point(dp, self._fp_spec, self._interface)
            for dp in raw_dps
        ]

        self._data_points = {dp.name(): dp for dp in dps}

    def name(self) -> str:
        if (
            self._fp_spec.functional_profile
            and self._fp_spec.functional_profile.functional_profile_name
        ):
            return self._fp_spec.functional_profile.functional_profile_name
        return ''

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        return self._data_points

    def get_specification(self) -> MessagingFunctionalProfileSpec:
        return self._fp_spec


class SGrMessagingInterface(SGrBaseInterface):
    """
    SmartGridready External Interface Class for Messaging Protocols
    """

    def __init__(
        self, frame: DeviceFrame
    ):
        super().__init__(frame)

        if (
            self.device_frame.interface_list
            and self.device_frame.interface_list
            and self.device_frame.interface_list.messaging_interface
        ):
            self._raw_interface = (
                self.device_frame.interface_list.messaging_interface
            )
        else:
            raise Exception('No messaging interface')
        desc = self._raw_interface.messaging_interface_description
        if desc is None:
            raise Exception('No messaging interface description')

        # configure interface
        self._client = get_messaging_client(str(self.device_frame.device_name), desc)
        self._client.set_message_handler(self.handle_client_message)  # type: ignore

        # subscribe to topic once, multiple handlers
        self._subscribed_topics: set[str] = set()
        self._data_point_handlers: list[tuple[str, str, str, Callable[[Any], NoReturn], Optional[MessagingFilter]]] = list()

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [MessagingFunctionalProfile(profile, self) for profile in raw_fps]
        self.functional_profiles = {fp.name(): fp for fp in fps}

    def is_connected(self):
        return self._client.is_connected()

    async def disconnect_async(self):
        for topic in self._subscribed_topics:
            await self._client.unsubscribe_async(topic)
        await self._client.disconnect()

    async def connect_async(self):
        await self._client.connect()
        for topic in self._subscribed_topics:
            await self._client.subscribe_async(topic)

    async def read_message(self, out_topic: str, in_topic: str, payload: Any) -> Any:
        # TODO implement active read - at the moment it will just receive value via DP handler
        await self._client.publish_async(out_topic, payload)

    async def write_message(self, topic: str, payload: Any):
        await self._client.publish_async(topic, payload)

    def data_point_handler(self, data_point: tuple[str, str, str, Callable[[Any], NoReturn], Optional[MessagingFilter]]):
        self._data_point_handlers.append(data_point)
        self._subscribed_topics.add(data_point[2])

    def handle_client_message(self, topic: str, payload: Any):
        # apply filter and notify data point subscribers
        for handler in filter(lambda d: d[2] == topic, self._data_point_handlers):
            if handler[4] is None or handler[4].is_filter_match(payload):
                handler[3](payload)
