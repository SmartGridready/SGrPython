from asyncio import run
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from sgr_specification.v0.generic import DataDirectionProduct, DeviceCategory
from sgr_specification.v0.product.product import DeviceFrame

from sgr_commhandler.api import DataPoint
from sgr_commhandler.api.configuration_parameter import (
    ConfigurationParameter,
    build_configurations_parameters,
)
from sgr_commhandler.api.data_types import DataTypes
from sgr_commhandler.api.functional_profile_api import FunctionalProfile


@dataclass
class DeviceInformation:
    name: str
    manufacturer: str
    software_revision: str
    hardware_revision: str
    device_category: DeviceCategory
    is_local: bool


class SGrBaseInterface(Protocol):
    frame: DeviceFrame
    configurations_params: list[ConfigurationParameter]
    device_information: DeviceInformation
    function_profiles: Mapping[str, FunctionalProfile]

    def _inititalize_device(
        self, frame: DeviceFrame
    ):
        self.frame = frame
        self.configurations_params = build_configurations_parameters(
            frame.configuration_list
        )
        self.device_information = DeviceInformation(
            name=frame.device_name if frame.device_name else '',
            manufacturer=frame.manufacturer_name
            if frame.manufacturer_name
            else '',
            software_revision=frame.device_information.software_revision
            if frame.device_information
            and frame.device_information.software_revision
            else '',
            hardware_revision=frame.device_information.hardware_revision
            if frame.device_information
            and frame.device_information.hardware_revision
            else '',
            device_category=frame.device_information.device_category
            if frame.device_information
            and frame.device_information.device_category
            else DeviceCategory.DEVICE_INFORMATION,
            is_local=frame.device_information.is_local_control
            if frame.device_information
            and frame.device_information.is_local_control
            else False,
        )

    def connect(self):
        run(self.connect_async())

    async def connect_async(self): ...

    def disconnect(self):
        run(self.disconnect_async())

    async def disconnect_async(self): ...

    def is_connected(self) -> bool: ...

    def get_function_profile(
        self, function_profile_name: str
    ) -> FunctionalProfile:
        return self.function_profiles[function_profile_name]

    def get_data_point(self, dp: tuple[str, str]) -> DataPoint:
        return self.get_function_profile(dp[0]).get_data_point(dp[1])

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        data_points = {}
        for fp in self.function_profiles.values():
            data_points.update(fp.get_data_points())
        return data_points

    def get_values(self) -> dict[tuple[str, str], Any]:
        return run(self.get_values_async())

    async def get_values_async(self) -> dict[tuple[str, str], Any]:
        data = {}
        for fp in self.function_profiles.values():
            data.update(
                {
                    (fp.name(), key): value
                    for key, value in (await fp.get_value_async()).items()
                }
            )
        return data

    def describe(
        self,
    ) -> tuple[
        str, dict[str, dict[str, tuple[DataDirectionProduct, DataTypes]]]
    ]:
        data = {}
        for fp in self.function_profiles.values():
            key, dps = fp.describe()
            data[key] = dps
        return self.device_information.name, data
