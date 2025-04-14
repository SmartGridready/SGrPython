from asyncio import run
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from sgr_specification.v0.generic import DataDirectionProduct, DeviceCategory
from sgr_specification.v0.product.product import DeviceFrame

from sgr_commhandler.api import DataPoint
from sgr_commhandler.api.configuration_parameter import (
    ConfigurationParameter,
    build_configuration_parameters,
)
from sgr_commhandler.api.data_types import DataTypes
from sgr_commhandler.api.functional_profile_api import FunctionalProfile


@dataclass
class DeviceInformation:
    """
    Implements a device information container.

    Attributes
    ----------
    name : str
        Defines the device name
    manufacturer : str
        Defines the manufacturer's name
    software_revision : str
        Defines the device software version
    hardware_revision : str
        Defines the device hardware version
    device_category : DeviceCategory
        Defines the device category
    is_local : bool
        Defines if the device is controlled locally or via cloud
    """
    name: str
    manufacturer: str
    software_revision: str
    hardware_revision: str
    device_category: DeviceCategory
    is_local: bool


class SGrBaseInterface(Protocol):
    """
    Defines an abstract base class for all SGr device interfaces.

    Attributes
    ----------
    device_frame : DeviceFrame
        the device specification
    configuration_parameters : list[ConfigurationParameter]
        the configuration parameters with default values
    device_information : DeviceInformation
        the device information
    functional_profiles : Mapping[str, FunctionalProfile]
        the configured functional profiles
    """
    device_frame: DeviceFrame
    configuration_parameters: list[ConfigurationParameter]
    device_information: DeviceInformation
    functional_profiles: Mapping[str, FunctionalProfile]

    def _inititalize_device(
        self, frame: DeviceFrame
    ):
        self.device_frame = frame
        self.configuration_parameters = build_configuration_parameters(
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
        """
        Connects the device synchronously.
        """
        run(self.connect_async())

    async def connect_async(self):
        """
        Connects the device asynchronously.
        """
        ...

    def disconnect(self):
        """
        Disconnects the device synchronously.
        """
        run(self.disconnect_async())

    async def disconnect_async(self):
        """
        Disconnects the device asynchronously.
        """
        ...

    def is_connected(self) -> bool:
        """
        Gets the connection state.

        Returns
        -------
        bool
            the connection state
        """
        ...

    def get_functional_profile(
        self, functional_profile_name: str
    ) -> FunctionalProfile:
        """
        Gets a functional profile.

        Parameters
        ----------
        functional_profile_name : str
            the functional profile name

        Returns
        -------
        FunctionalProfile
            a functional profile
        """
        return self.functional_profiles[functional_profile_name]

    def get_data_point(self, dp: tuple[str, str]) -> DataPoint:
        """
        Gets a data point.

        Parameters
        ----------
        dp : tuple[str, str]
            the functional profile and data point name

        Returns
        -------
        DataPoint
            a data point
        """
        return self.get_functional_profile(dp[0]).get_data_point(dp[1])

    def get_data_points(self) -> dict[tuple[str, str], DataPoint]:
        """
        Gets all data points.

        Returns
        -------
        dict[tuple[str, str], DataPoint]
            all data points
        """
        data_points = {}
        for fp in self.functional_profiles.values():
            data_points.update(fp.get_data_points())
        return data_points

    def get_values(self) -> dict[tuple[str, str], Any]:
        """
        Gets all data point values synchronously.

        Returns
        -------
        dict[tuple[str, str], Any]
            all data point values
        """
        return run(self.get_values_async())

    async def get_values_async(self) -> dict[tuple[str, str], Any]:
        """
        Gets all data point values asynchronously.

        Returns
        -------
        dict[tuple[str, str], Any]
            all data point values
        """
        data = {}
        for fp in self.functional_profiles.values():
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
        """
        Gets the device description and all data.

        Returns
        -------
        tuple[str, dict[str, dict[str, tuple[DataDirectionProduct, DataTypes]]]]
            a tuple of device name and all data point values
        """
        data = {}
        for fp in self.functional_profiles.values():
            key, dps = fp.describe()
            data[key] = dps
        return self.device_information.name, data
