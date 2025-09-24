from collections.abc import Callable
from typing import Any, Generic, Optional, Protocol, TypeVar

from sgr_specification.v0.generic import DataDirectionProduct, Units, DataPointBase

from sgr_commhandler.api.dynamic_parameter import DynamicParameter
from sgr_commhandler.api.data_types import DataTypes
from sgr_commhandler.api.value import DataPointValue

"""Defines a generic data type."""
TDpSpec = TypeVar('TDpSpec', covariant=True, bound=DataPointBase)


class DataPointValidator(Protocol):
    """
    Implements a base class for data point validators.
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

    def transform_to_generic(self, value: Any) -> Any:
        """
        Transforms the value to a generic type, if necessary.

        Parameters
        ----------
        value : Any
            the value to validate

        Returns
        -------
        Any
            the transformed value
        """
        return value

    def transform_to_device(self, value: Any) -> Any:
        """
        Transforms the value to a device type, if necessary.

        Parameters
        ----------
        value : Any
            the value to validate

        Returns
        -------
        Any
            the transformed value
        """
        return value


class DataPointConsumer(object):
    """
    Wraps a consumer function for data point values.
    """
    def __init__(self, consume: Callable[[DataPointValue], None], validator: DataPointValidator):
        self._consume = consume
        self._validator = validator
    
    def consume(self, value: Any):
        """
        Validates the incoming value and calls the consumer function.

        Parameters
        ----------
        value : Any
            the value to consume
        """
        if self._validator.validate(value):
            sgr_value = self._validator.transform_to_generic(value)
            self._consume(DataPointValue(sgr_value, self._validator.data_type()))
        raise Exception(
            f"invalid value read from device, {value}, validator: {self._validator.data_type()}"
        )


class DataPointProtocol(Protocol[TDpSpec]):
    """
    Implements a base class for data point protocols.
    """
    def get_specification(self) -> TDpSpec:
        """
        Gets the data point specification.
        
        Returns
        -------
        TDpSpec
            the interface-specific specification
        """
        ...

    async def set_val(self, value: Any):
        """
        Writes the data point value.

        Parameters
        ----------
        value : Any
            the data point value to write
        """
        ...

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
        ...

    def direction(self) -> DataDirectionProduct:
        """
        Gets the data direction of the data point.

        Returns
        -------
        DataDirectionProduct
            the data point direction
        """
        ...

    def unit(self) -> Units:
        """
        Gets the unit of measurement of the data point.

        Returns
        -------
        Units
            the unit
        """
        ...

    def dynamic_parameters(self) -> list[DynamicParameter]:
        """
        Gets the dynamic parameters of the data point.

        Returns
        -------
        list[DynamicParameter]
            the dynamic parameters
        """
        return []

    def can_subscribe(self) -> bool:
        """
        Defines if subscribe() is allowed.

        Returns
        -------
        bool
            True if allowed, False otherwise
        """
        return False

    def subscribe(self, consumer: DataPointConsumer):
        """
        Subscribes to changes of the data point value.

        Parameters
        ----------
        consumer : DataPointConsumer
            the callback handler
        """
        raise Exception('Unsupported operation')

    def unsubscribe(self):
        """
        Unsubscribes from changes of the data point value.
        """
        raise Exception('Unsupported operation')


class DataPoint(Generic[TDpSpec]):
    """
    Implements a data point of a generic data type.
    """

    def __init__(
        self, protocol: DataPointProtocol[TDpSpec], validator: DataPointValidator
    ):
        """
        Constructs a data point.

        Parameters
        ----------
        protocol : DataPointProtocol[TDpSpec]
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

    async def get_value_async(self, parameters: Optional[dict[str, str]] = None) -> DataPointValue:
        """
        Gets the data point value asynchronously.

        Returns
        -------
        DataPointValue
            the data point value
        
        Raises
        ------
        Exception
            when read value is not compatible with data type
        """
        value = await self._protocol.get_val(parameters)
        if self._validator.validate(value):
            sgr_value = self._validator.transform_to_generic(value)
            return DataPointValue(sgr_value, self._validator.data_type())
        raise Exception(
            f"invalid value read from device, {value}, validator: {self._validator.data_type()}"
        )

    async def set_value_async(self, value: DataPointValue):
        """
        Sets the data point value asynchronously.

        Parameters
        ----------
        value: DataPointValue
            the data point value
        """
        if self._validator.validate(value.value):
            dev_value = self._validator.transform_to_device(value.value)
            return await self._protocol.set_val(dev_value)
        raise Exception('invalid data to write to device')

    def subscribe(self, fn: Callable[[DataPointValue], None]):
        """
        Subscribes to data point value changes.

        Parameters
        ----------
        fn : Callable[[DataPointValue], None]
            the handler method
        """
        self._protocol.subscribe(DataPointConsumer(fn, self._validator))

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
