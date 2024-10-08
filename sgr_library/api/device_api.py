from abc import ABC, abstractmethod
from asyncio import run
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sgrspecification.generic import DataDirectionProduct, DeviceCategory

from sgr_library.api import DataPoint
from sgr_library.api.configuration_parameter import ConfigurationParameter
from sgr_library.api.data_types import DataTypes
from sgr_library.api.function_profile_api import FunctionProfile


@dataclass
class DeviceInformation:
    name: str
    manufacture: str
    software_revision: str
    hardware_revision: str
    device_category: DeviceCategory
    is_local: bool


class BaseSGrInterface(ABC):
    def connect(self):
        run(self.connect_async())

    @abstractmethod
    async def connect_async(self):
        pass

    def disconnect(self):
        run(self.disconnect_async())

    @abstractmethod
    async def disconnect_async(self):
        pass

    @abstractmethod
    def get_function_profiles(self) -> Mapping[str, FunctionProfile]:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def device_information(self) -> DeviceInformation:
        pass

    @abstractmethod
    def configuration_parameter(self) -> list[ConfigurationParameter]:
        pass

    def get_function_profile(
        self, function_profile_name: str
    ) -> FunctionProfile:
        return self.get_function_profiles()[function_profile_name]

    def get_data_point(self, dp: tuple[str, str]) -> DataPoint:
        return self.get_function_profile(dp[0]).get_data_point(dp[1])

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        data_points = {}
        for fp in self.get_function_profiles().values():
            data_points.update(fp.get_data_points())
        return data_points

    def get_value(self) -> dict[tuple[str, str], Any]:
        return run(self.get_value_async())

    async def get_value_async(self) -> dict[tuple[str, str], Any]:
        data = {}
        for fp in self.get_function_profiles().values():
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
        for fp in self.get_function_profiles().values():
            key, dps = fp.describe()
            data[key] = dps
        return self.device_information().name, data
