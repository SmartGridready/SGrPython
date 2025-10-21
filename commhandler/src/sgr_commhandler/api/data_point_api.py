"""
Provides the data-point-level API.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Generic, NoReturn, Optional, TypeVar

from sgr_specification.v0.generic import DataDirectionProduct, Units, DataPointBase, FunctionalProfileBase

from sgr_commhandler.api.dynamic_parameter import DynamicParameter, build_dynamic_parameters
from sgr_commhandler.api.data_types import DataTypes


TFpSpec = TypeVar('TFpSpec', covariant=True, bound=FunctionalProfileBase)
"""Defines a generic functional profile data type."""

TDpSpec = TypeVar('TDpSpec', covariant=True, bound=DataPointBase)
"""Defines a generic data point data type."""


class DataPointValidator(object):
    """
    Implements a base class for data point validators.
    """

    _data_type: DataTypes

    def __init__(self, data_type: DataTypes):
        self._data_type = data_type

    def validate(self, value: Any) -> bool:
        """
        Validates the compatibility of a value.

        Parameters
        ----------
        value : Any
            the value to validate

        Returns
        -------
        bool
            true if value is compatible, false otherwise
        """
        return False

    def data_type(self) -> DataTypes:
        """
        Gets the validator's data type.

        Returns
        -------
        DataTypes
            the data type enumeration
        """
        return self._data_type

    def options(self) -> list[Any]:
        """
        Gets the validator's options.

        Returns
        -------
        list[Any]
            the options
        """
        return []


class DataPointProtocol(ABC, Generic[TFpSpec, TDpSpec]):
    """
    Implements a base class for data point protocols.
    """

    _fp_spec: TFpSpec
    _dp_spec: TDpSpec
    _fp_name: str
    _dp_name: str
    _dynamic_parameters: list[DynamicParameter]

    def __init__(self, fp_spec: TFpSpec, dp_spec: TDpSpec):
        self._fp_spec = fp_spec
        self._dp_spec = dp_spec

        self._fp_name = fp_spec.functional_profile.functional_profile_name if (
            fp_spec.functional_profile is not None
            and fp_spec.functional_profile.functional_profile_name is not None
        ) else ''

        self._dp_name = dp_spec.data_point.data_point_name if (
            dp_spec.data_point is not None
            and dp_spec.data_point.data_point_name is not None
        ) else ''

        self._dynamic_parameters = build_dynamic_parameters(
            self._dp_spec.data_point.parameter_list
            if self._dp_spec.data_point
            else None
        )

    def get_specification(self) -> TDpSpec:
        """
        Gets the data point specification.

        Returns
        -------
        TDpSpec
            the interface-specific specification
        """
        return self._dp_spec

    @abstractmethod
    async def set_val(self, value: Any):
        """
        Writes the data point value.

        Parameters
        ----------
        value : Any
            the data point value to write
        """
        ...

    @abstractmethod
    async def get_val(self, parameters: Optional[dict[str, str]] = None, skip_cache: bool = False) -> Any:
        """
        Reads the data point value.

        Parameters
        ----------
        parameters : Optional[dict[str, str]]
            optional dynamic parameters of the request
        skip_cache : bool
            does not use cache if true

        Returns
        -------
        Any
            the data point value
        """
        ...

    def name(self) -> tuple[str, str]:
        """
        Gets the functional profile and data point names.

        Returns
        -------
        tuple[str, str]
            the functional profile and data point names as tuple
        """
        return (self._fp_name, self._dp_name)

    def direction(self) -> DataDirectionProduct:
        """
        Gets the data direction of the data point.

        Returns
        -------
        DataDirectionProduct
            the data point direction
        """
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.data_direction is None
        ):
            raise Exception('missing data direction')
        return self._dp_spec.data_point.data_direction

    def unit(self) -> Units:
        """
        Gets the unit of measurement of the data point.

        Returns
        -------
        Units
            the unit
        """
        if (
            self._dp_spec.data_point is None
            or self._dp_spec.data_point.unit is None
        ):
            return Units.NONE
        return self._dp_spec.data_point.unit

    def dynamic_parameters(self) -> list[DynamicParameter]:
        """
        Gets the dynamic parameters of the data point.

        Returns
        -------
        list[DynamicParameter]
            the dynamic parameters
        """
        return self._dynamic_parameters

    def can_subscribe(self) -> bool:
        """
        Defines if subscribe() is allowed.

        Returns
        -------
        bool
            True if allowed, False otherwise
        """
        return False

    def subscribe(self, fn: Callable[['DataPointProtocol', Any], NoReturn]):
        """
        Subscribes to changes of the data point value.

        Parameters
        ----------
        fn : Callable[[DataPointProtocol, Any], NoReturn]
            the callback method
        """
        raise Exception('subscribe() is not supported')

    def unsubscribe(self):
        """
        Unsubscribes from changes of the data point value.
        """
        raise Exception('unsubscribe() is not supported')


class DataPoint(Generic[TFpSpec, TDpSpec]):
    """
    Implements a data point of a generic data type.
    """

    def __init__(
        self, protocol: DataPointProtocol[TFpSpec, TDpSpec], validator: DataPointValidator
    ):
        """
        Constructs a data point.

        Parameters
        ----------
        protocol : DataPointProtocol[TFpSpec, TDpSpec]
            the underlying protocol
        validator : DataPointValidator
            the data point's value validator
        """
        self._protocol = protocol
        self._validator = validator

    def name(self) -> tuple[str, str]:
        """
        Gets the data point name.

        Returns
        -------
        tuple[str, str]
            the functional profile and data point name
        """
        return self._protocol.name()

    async def get_value_async(self, parameters: Optional[dict[str, str]] = None, skip_cache: bool = False) -> Any:
        """
        Gets the data point value asynchronously.

        Returns
        -------
        Any
            the data point value

        Raises
        ------
        Exception
            when read value is not compatible with data type
        """
        value = await self._protocol.get_val(parameters, skip_cache)
        if self._validator.validate(value):
            return value
        raise Exception(
            f'invalid value read from device, {value}, validator: {self._validator.data_type()}'
        )

    async def set_value_async(self, value: Any):
        """
        Sets the data point value asynchronously.

        Parameters
        ----------
        value: Any
            the data point value
        """
        if self._validator.validate(value):
            return await self._protocol.set_val(value)
        raise Exception('invalid data to write to device')

    def subscribe(self, fn: Callable[[DataPointProtocol, Any], NoReturn]):
        """
        Subscribes to data point value changes.

        Parameters
        ----------
        fn : Callable[[DataPointProtocol, Any], NoReturn]
            the handler method
        """
        self._protocol.subscribe(fn)

    def unsubscribe(self):
        """
        Unsubscribes from data point value changes.
        """
        self._protocol.unsubscribe()

    def direction(self) -> DataDirectionProduct:
        """
        Gets the data point direction.

        Returns
        -------
        DataDirectionProduct
            the data point direction
        """
        return self._protocol.direction()

    def data_type(self) -> DataTypes:
        """
        Gets the data point data type.

        Returns
        -------
        DataTypes
            the data point data type
        """
        return self._validator.data_type()

    def unit(self) -> Units:
        """
        Gets the unit of measurement of the data point.

        Returns
        -------
        Units
            the unit
        """
        return self._protocol.unit()

    def describe(
        self,
    ) -> tuple[tuple[str, str], DataDirectionProduct, DataTypes, Units]:
        """
        Describes the data point.

        Returns
        -------
        tuple[tuple[str, str], DataDirectionProduct, DataTypes, Units]
            the data point information
        """
        return self.name(), self.direction(), self.data_type(), self.unit()

    def options(self) -> list[Any]:
        """
        Describes the data point options.

        Returns
        -------
        list[Any]
            the data point options
        """
        return self._validator.options()

    def dynamic_parameters(self) -> list[DynamicParameter]:
        """
        Gets the dynamic parameters of the data point.

        Returns
        -------
        list[DynamicParameter]
            the dynamic parameters
        """
        return self._protocol.dynamic_parameters()

    def get_specification(self) -> TDpSpec:
        """
        Gets the data point specification.

        Returns
        -------
        TDpSpec
            the data point specification
        """
        return self._protocol.get_specification()
