from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from sgr_library.api import DataPoint
from sgr_library.api.function_profile_api import FunctionProfile
from sgr_library.data_classes.generic import DeviceCategory


@dataclass
class DeviceInformation:
    name: str
    manufacture: str
    software_revision: str
    hardware_revision: str
    device_category: DeviceCategory
    is_local: bool


class BaseSGrInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_function_profiles(self) -> dict[str, FunctionProfile]:
        pass

    @abstractmethod
    def device_information(self) -> DeviceInformation:
        pass

    def get_function_profile(self, function_profile_name: str) -> FunctionProfile:
        return self.get_function_profiles()[function_profile_name]

    def get_data_point(self, dp: tuple[str, str]) -> DataPoint:
        return self.get_function_profile(dp[0]).get_data_point(dp[1])

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        data_points = {}
        for fp in self.get_function_profiles().values():
            data_points.update(fp.get_data_points())
        return data_points

    async def read_data(self) -> dict[tuple[str, str], Any]:
        data = {}
        for fp in self.get_function_profiles().values():
            data.update(await fp.read())
        return data
