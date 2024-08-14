from abc import ABC, abstractmethod

from typing import Tuple, Dict
from sgr_library.api.data_point_api import DataPoint
from sgr_library.api.data_types import DataTypes
from sgrspecification.generic import DataDirectionProduct
from asyncio import run


class FunctionProfile(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_data_points(self) -> Dict[Tuple[str, str], DataPoint]:
        pass

    def get_data_point(self, dp_name: str) -> DataPoint:
        return self.get_data_points()[(self.name(), dp_name)]

    async def get_value_async(self) -> Dict[str, DataPoint]:
        return {key[1]: await dp.get_value_async() for key, dp in self.get_data_points().items()}

    def get_value(self) -> Dict[str, DataPoint]:
        return run(self.get_value_async())

    def describe(self) -> Tuple[str, Dict[str, Tuple[DataDirectionProduct, DataTypes]]]:
        infos = map(lambda dp: dp.describe(), self.get_data_points().values())
        return self.name(), {dp[0][1]: (dp[1], dp[2]) for dp in infos}
