import logging
from collections.abc import Callable
from typing import Any

from sgr_specification.v0.generic import DataDirectionProduct
from sgr_specification.v0.product import (
    DeviceFrame,
)
from sgr_specification.v0.product import (
    MessagingDataPoint as MessagingDataPointSpec,
)
from sgr_specification.v0.product import (
    MessagingFunctionalProfile as MessagingFunctionalProfileSpec,
)

from sgr_commhandler.api import (
    DataPoint,
    DataPointProtocol,
    FunctionalProfile,
    SGrBaseInterface,
)
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def build_messaging_data_point(
    data_point: MessagingDataPointSpec,
    function_profile: MessagingFunctionalProfileSpec,
    interface: 'SGrMessagingInterface',
) -> DataPoint:
    protocol = MessagingDataPoint(data_point, function_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


class MessagingDataPoint(DataPointProtocol):
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

        self._interface = interface

    def name(self) -> tuple[str, str]:
        return self._fp_name, self._dp_name

    async def get_val(self, skip_cache: bool = False):
        raise Exception('Not implemented')

    async def set_val(self, value: Any):
        raise Exception('Not implemented')

    def direction(self) -> DataDirectionProduct:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction

    def can_subscribe(self) -> bool:
        return True

    def subscribe(self, fn: Callable[[Any], None]):
        # TODO implement
        raise Exception('not implemented yet')

    def unsubscribe(self):
        # TODO implement
        raise Exception('not implemented yet')


class MessagingFunctionalProfile(FunctionalProfile):
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


class SGrMessagingInterface(SGrBaseInterface):
    """
    SmartGridready External Interface Class for Messaging Protocols
    """

    def __init__(
        self, frame: DeviceFrame
    ):
        self._inititalize_device(frame)

        if (
            self.frame.interface_list
            and self.frame.interface_list
            and self.frame.interface_list.messaging_interface
        ):
            self._raw_interface = (
                self.frame.interface_list.messaging_interface
            )
        else:
            raise Exception('No messaging interface')
        desc = self._raw_interface.messaging_interface_description
        if desc is None:
            raise Exception('No messaging interface description')

        # TODO configure interface

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [MessagingFunctionalProfile(profile, self) for profile in raw_fps]
        self.function_profiles = {fp.name(): fp for fp in fps}

    def is_connected(self):
        return False

    async def disconnect_async(self):
        # TODO implement
        pass

    async def connect_async(self):
        # TODO implement
        pass
