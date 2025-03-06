import logging
from typing import Any

from sgr_specification.v0.generic import (
    DataDirectionProduct,
)
from sgr_specification.v0.generic import (
    DataPointBase as ContactDataPointSpec,
)
from sgr_specification.v0.product import (
    ContactFunctionalProfile as ContactFunctionalProfileSpec,
)
from sgr_specification.v0.product import (
    DeviceFrame,
)

from sgr_commhandler.api import (
    DataPoint,
    DataPointProtocol,
    FunctionalProfile,
    SGrBaseInterface,
)
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def build_contact_data_point(
    data_point: ContactDataPointSpec,
    function_profile: ContactFunctionalProfileSpec,
    interface: 'SGrContactInterface',
) -> DataPoint:
    protocol = ContactDataPoint(data_point, function_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


class ContactDataPoint(DataPointProtocol):
    def __init__(
        self,
        dp_spec: ContactDataPointSpec,
        fp_spec: ContactFunctionalProfileSpec,
        interface: 'SGrContactInterface',
    ):
        self._dp_spec = dp_spec
        self._fp_spec = fp_spec

        self._fp_name = ''
        if (
            fp_spec.functional_profile is not None
            and fp_spec.functional_profile.functional_profile_name is not None
        ):
            self._fp_name = fp_spec.functional_profile.functional_profile_name

        self._dp_name = ''
        if (
            self._dp_spec.data_point is not None
            and self._dp_spec.data_point.data_point_name is not None
        ):
            self._dp_name = self._dp_spec.data_point.data_point_name

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


class ContactFunctionalProfile(FunctionalProfile):
    def __init__(
        self,
        fp_spec: ContactFunctionalProfileSpec,
        interface: 'SGrContactInterface',
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
            build_contact_data_point(dp, self._fp_spec, self._interface)
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


class SGrContactInterface(SGrBaseInterface):
    """
    SmartGridready External Interface Class for Contact Protocols
    Note: we do not implement a complete driver here, because it is very application-dependent!
    """

    def __init__(
        self, frame: DeviceFrame
    ):
        self._inititalize_device(frame)

        if (
            self.frame.interface_list
            and self.frame.interface_list
            and self.frame.interface_list.contact_interface
        ):
            self._raw_interface = self.frame.interface_list.contact_interface
        else:
            raise Exception('No contact interface')
        desc = self._raw_interface.contact_interface_description
        if desc is None:
            raise Exception('No contact interface description')

        # TODO configure interface
        self.number_of_contacts = desc.number_of_contacts
        self.contact_stabilization_time = desc.contact_stabilisation_time_ms

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [ContactFunctionalProfile(profile, self) for profile in raw_fps]
        self.function_profiles = {fp.name(): fp for fp in fps}

    def is_connected(self):
        return False

    async def disconnect_async(self):
        # TODO implement after "driver"
        pass

    async def connect_async(self):
        # TODO implement after "driver"
        pass
