import logging
from typing import Any

from sgr_specification.v0.generic import (
    DataDirectionProduct,
)
from sgr_specification.v0.generic import (
    DataPointBase as GenericDataPointSpec,
)
from sgr_specification.v0.product import (
    DeviceFrame,
)
from sgr_specification.v0.product import (
    GenericFunctionalProfile as GenericFunctionalProfileSpec,
)

from sgr_commhandler.api import (
    DataPoint,
    DataPointProtocol,
    FunctionalProfile,
    SGrBaseInterface,
)
from sgr_commhandler.validators import build_validator

logger = logging.getLogger(__name__)


def build_generic_data_point(
    data_point: GenericDataPointSpec,
    function_profile: GenericFunctionalProfileSpec,
    interface: 'SGrGenericInterface',
) -> DataPoint:
    protocol = GenericDataPoint(data_point, function_profile, interface)
    data_type = None
    if data_point.data_point and data_point.data_point.data_type:
        data_type = data_point.data_point.data_type
    validator = build_validator(data_type)
    return DataPoint(protocol, validator)


class GenericDataPoint(DataPointProtocol):
    def __init__(
        self,
        dp_spec: GenericDataPointSpec,
        fp_spec: GenericFunctionalProfileSpec,
        interface: 'SGrGenericInterface',
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
        # supports at least constant DPs
        if (
            self._dp_spec.data_point
            and self._dp_spec.data_point.data_direction
            is DataDirectionProduct.C
        ):
            return self._dp_spec.data_point.value
        raise Exception('Not supported')

    async def set_val(self, value: Any):
        raise Exception('Not supported')

    def direction(self) -> DataDirectionProduct:
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction


class GenericFunctionalProfile(FunctionalProfile):
    def __init__(
        self,
        fp_spec: GenericFunctionalProfileSpec,
        interface: 'SGrGenericInterface',
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
            build_generic_data_point(dp, self._fp_spec, self._interface)
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


class SGrGenericInterface(SGrBaseInterface):
    """
    SmartGridready External Interface Class for Generic Protocols
    Actually has no communication protocol, just generic data
    """

    def __init__(
        self, frame: DeviceFrame
    ):
        self._inititalize_device(frame)

        if (
            self.frame.interface_list
            and self.frame.interface_list
            and self.frame.interface_list.generic_interface
        ):
            self._raw_interface = self.frame.interface_list.generic_interface
        else:
            raise Exception('No generic interface')

        raw_fps = []
        if (
            self._raw_interface.functional_profile_list
            and self._raw_interface.functional_profile_list.functional_profile_list_element
        ):
            raw_fps = self._raw_interface.functional_profile_list.functional_profile_list_element
        fps = [GenericFunctionalProfile(profile, self) for profile in raw_fps]
        self.function_profiles = {fp.name(): fp for fp in fps}

    def is_connected(self):
        return False

    async def disconnect_async(self):
        pass

    async def connect_async(self):
        pass
