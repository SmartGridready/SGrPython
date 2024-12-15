from asyncio import run
from asyncio.protocols import Protocol

from sgr_specification.v0.generic import DataDirectionProduct

from sgr_commhandler.api.data_point_api import DataPoint
from sgr_commhandler.api.data_types import DataTypes


class FunctionalProfile(Protocol):
    def name(self) -> str: ...

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]: ...

    def get_data_point(self, dp_name: str) -> DataPoint:
        return self.get_data_points()[(self.name(), dp_name)]

    async def get_value_async(self) -> dict[str, DataPoint]:
        return {
            key[1]: await dp.get_value_async()
            for key, dp in self.get_data_points().items()
        }

    def get_value(self) -> dict[str, DataPoint]:
        return run(self.get_value_async())

    def describe(
        self,
    ) -> tuple[str, dict[str, tuple[DataDirectionProduct, DataTypes]]]:
        infos = map(lambda dp: dp.describe(), self.get_data_points().values())
        return self.name(), {dp[0][1]: (dp[1], dp[2]) for dp in infos}
