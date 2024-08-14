from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple, Dict

from sgr_library.api import DataPoint
from sgr_library.api.configuration_parameter import ConfigurationParameter
from sgr_library.api.data_types import DataTypes
from sgr_library.api.function_profile_api import FunctionProfile
from sgr_library.generated.generic import DeviceCategory, DataDirectionProduct


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
    async def connect_async(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    async def disconnect_async(self):
        pass

    @abstractmethod
    def get_function_profiles(self) -> Dict[str, FunctionProfile]:
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def device_information(self) -> DeviceInformation:
        pass

    @abstractmethod
    def configuration_parameter(self) -> list[ConfigurationParameter]:
        pass

    def get_function_profile(self, function_profile_name: str) -> FunctionProfile:
        return self.get_function_profiles()[function_profile_name]

    def get_data_point(self, dp: Tuple[str, str]) -> DataPoint:
        return self.get_function_profile(dp[0]).get_data_point(dp[1])

    def get_data_points(self) -> Dict[Tuple[str, str], DataPoint]:
        data_points = {}
        for fp in self.get_function_profiles().values():
            data_points.update(fp.get_data_points())
        return data_points


    def get_value(self) ->  Dict[Tuple[str, str], Any]:
        pass

    async def get_value_async(self) -> Dict[Tuple[str, str], Any]:
        data = {}
        for fp in self.get_function_profiles().values():
            data.update({(fp.name(), key): value for key, value in (await fp.read()).items()})
        return data

    def describe(self) -> Tuple[str, Dict[str, Dict[str, Tuple[DataDirectionProduct, DataTypes]]]]:

        data = {}
        for fp in self.get_function_profiles().values():
            key, dps = fp.describe()
            data[key] = dps
        return self.device_information().name, data
