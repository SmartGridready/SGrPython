from asyncio import run
from asyncio.protocols import Protocol

from sgr_specification.v0.generic import DataDirectionProduct

from sgr_commhandler.api.data_point_api import DataPoint
from sgr_commhandler.api.data_types import DataTypes


class FunctionalProfile(Protocol):
    """
    Implements a functional profile.
    """

    def name(self) -> str:
        """
        Gets the functional profile name.

        Returns
        -------
        str
            the functional profile name
        """
        ...

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        """
        Gets all data points.

        Returns
        -------
        dict[tuple[str, str], DataPoint]
            all data points
        """
        ...

    def get_data_point(self, dp_name: str) -> DataPoint:
        """
        Gets a data point.

        Parameters
        ----------
        dp_name : str
            the data point name

        Returns
        -------
        DataPoint
            a data point
        """
        return self.get_data_points()[(self.name(), dp_name)]

    async def get_value_async(self) -> dict[str, DataPoint]:
        """
        Gets all data point values of the functional profile asynchronously.

        Returns
        -------
        dict[str, DataPoint]
            all data point values by name
        """
        return {
            key[1]: await dp.get_value_async()
            for key, dp in self.get_data_points().items()
        }

    def get_value(self) -> dict[str, DataPoint]:
        """
        Gets all data point values of the functional profile synchronously.

        Returns
        -------
        dict[str, DataPoint]
            all data point values by name
        """
        return run(self.get_value_async())

    def describe(
        self,
    ) -> tuple[str, dict[str, tuple[DataDirectionProduct, DataTypes]]]:
        """
        Describes the functional profile.

        Returns
        -------
        tuple[str, dict[str, tuple[DataDirectionProduct, DataTypes]]]
            the functional profile information
        """
        infos = map(lambda dp: dp.describe(), self.get_data_points().values())
        return self.name(), {dp[0][1]: (dp[1], dp[2]) for dp in infos}
