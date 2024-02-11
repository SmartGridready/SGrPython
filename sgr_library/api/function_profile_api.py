from abc import ABC, abstractmethod

from sgr_library.api.data_point_api import DataPoint


class FunctionProfile(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        pass

    def get_data_point(self, dp_name: str) -> DataPoint:
        return self.get_data_points()[(self.name(), dp_name)]

    async def read(self) -> dict[str, DataPoint]:
        return {key[1]: await dp.read() for key, dp in self.get_data_points().items()}
