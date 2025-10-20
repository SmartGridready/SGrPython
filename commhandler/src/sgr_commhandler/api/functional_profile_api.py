from typing import Any, Generic, Optional, TypeVar

from sgr_specification.v0.generic import DataDirectionProduct
from sgr_specification.v0.generic.functional_profile import FunctionalProfileBase

from sgr_commhandler.api.data_point_api import DataPoint
from sgr_commhandler.api.data_types import DataTypes


TFpSpec = TypeVar('TFpSpec', covariant=True, bound=FunctionalProfileBase)
"""Defines a generic functional profile data type."""


class FunctionalProfile(Generic[TFpSpec]):
    """
    Implements a functional profile.
    """

    _fp_spec: TFpSpec

    def __init__(self, fp_spec: TFpSpec):
        self._fp_spec = fp_spec

    def name(self) -> str:
        """
        Gets the functional profile name.

        Returns
        -------
        str
            the functional profile name
        """
        if (
            self._fp_spec.functional_profile
            and self._fp_spec.functional_profile.functional_profile_name
        ):
            return self._fp_spec.functional_profile.functional_profile_name
        return ''

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

    async def get_values_async(self, parameters: Optional[dict[str, str]] = None) -> dict[str, Any]:
        """
        Gets all data point values of the functional profile asynchronously.

        Returns
        -------
        dict[str, Any]
            all data point values by name
        """
        data: dict[str, Any] = dict()
        for (key, dp) in self.get_data_points().items():
            try:
                value = await dp.get_value_async(parameters)
                data[key[1]] = value
            except Exception:
                # TODO log error - None should not be a valid DP value
                data[key[1]] = None
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

    def get_specification(self) -> TFpSpec:
        """
        Gets the functional profile specification.

        Returns
        -------
        TFpSpec
            the functional profile specification
        """
        return self._fp_spec
