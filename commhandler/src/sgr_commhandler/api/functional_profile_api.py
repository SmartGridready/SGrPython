from typing import Optional, Protocol

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

    async def get_values_async(self, parameters: Optional[dict[str, str]] = None) -> dict[str, DataPoint]:
        """
        Gets all data point values of the functional profile asynchronously.

        Returns
        -------
        dict[str, DataPoint]
            all data point values by name
        """
        data = {}
        for key, dp in self.get_data_points().items():
            try:
                value = await dp.get_value_async(parameters)
                data[key] = value
            except Exception as e:
                # TODO log error - None should not be a valid DP value
                data[key] = None
        return data

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
