from asyncio import run
from collections.abc import Callable
from typing import Any, Generic, Protocol, TypeVar

from sgr_specification.v0.generic import DataDirectionProduct, Units

from sgr_commhandler.api.data_types import DataTypes

"""Defines a generic data type."""
T = TypeVar('T')


class DataPointValidator(Protocol):
    """
    Defines an interface for data point validators.
    """

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

        ...

    def data_type(self) -> DataTypes:
        """
        Gets the validator's data type.

        Returns
        -------
        DataTypes
            the data type enumeration
        """

        ...

    def options(self) -> list[Any]:
        """
        Gets the validator's options.

        Returns
        -------
        list[Any]
            the options
        """

        return []


class DataPointProtocol(Protocol):
    """
    Defines an interface for data point protocols.
    """

    async def set_val(self, value: Any):
        """
        Writes the data point value.

        Parameters
        ----------
        value : Any
            the data point value to write
        """

        ...

    async def get_val(self, skip_cache: bool = False) -> Any:
        """
        Reads the data point value.

        Parameters
        ----------
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

        ...

    def direction(self) -> DataDirectionProduct:
        """
        Gets the data direction of the data point.

        Returns
        -------
        DataDirectionProduct
            the functional profile and data point names as tuple
        """

        ...

    def unit(self) -> Units:
        ...

    def can_subscribe(self) -> bool:
        """
        Defines if subscribe() is allowed.

        Returns
        -------
        bool
            True if allowed, False otherwise
        """

        return False

    def subscribe(self, fn: Callable[[Any], None]):
        """
        Subscribes to changes of the data point value.

        Parameters
        ----------
        fn : Callable[[Any], None]
            the callback method
        """

        raise Exception('Unsupported operation')

    def unsubscribe(self):
        """
        Unsubscribes from changes of the data point value.
        """

        raise Exception('Unsupported operation')


class DataPoint(Generic[T]):
    """
    Implements a data point of a generic data type.
    """

    def __init__(
        self, protocol: DataPointProtocol, validator: DataPointValidator
    ):
        """
        Constructs a data point.

        Parameters
        ----------
        protocol : DataPointProtocol
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

    async def get_value_async(self) -> T:
        """
        Gets the data point value asynchronously.

        Returns
        -------
        T
            the data point value
        
        Raises
        ------
        Exception
            when read value is not compatible with data type
        """

        value = await self._protocol.get_val()
        if self._validator.validate(value):
            return value
        raise Exception(
            f'invalid value read from device, {value}, validator: {self._validator.data_type()}'
        )

    def get_value(self) -> T:
        """
        Gets the data point value synchronously.

        Returns
        -------
        T
            the data point value
        
        Raises
        ------
        Exception
            when read value is not compatible with data type
        """

        return run(self.get_value_async())

    async def set_value_async(self, value: T):
        """
        Sets the data point value asynchronously.

        Parameters
        ----------
        value: T
            the data point value
        """

        if self._validator.validate(value):
            return await self._protocol.set_val(value)
        raise Exception('invalid data to write to device')

    def set_value(self, value: T):
        """
        Sets the data point value synchronously.

        Parameters
        ----------
        value: T
            the data point value
        """

        return run(self.set_value_async(value))

    def subscribe(self, fn: Callable[[Any], None]):
        """
        Subscribes to data point value changes.

        Parameters
        ----------
        fn : Callable[[Any], None]
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
