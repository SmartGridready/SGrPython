from asyncio import run
from collections.abc import Callable
from typing import Any, Generic, Protocol, TypeVar

from sgr_specification.v0.generic import DataDirectionProduct

from sgr_commhandler.api.data_types import DataTypes

T = TypeVar('T')


class DataPointValidator(Protocol):
    def validate(self, value: Any) -> bool: ...

    def data_type(self) -> DataTypes: ...

    def options(self) -> list[Any] | None:
        return None


class DataPointProtocol(Protocol):
    async def set_val(self, value: Any): ...

    async def get_val(self, skip_cache: bool = False) -> Any: ...

    def name(self) -> tuple[str, str]: ...

    def direction(self) -> DataDirectionProduct: ...

    def can_subscribe(self) -> bool:
        return False

    def subscribe(self, fn: Callable[[Any], None]):
        raise Exception('Unsupported operatioin')

    def unsubscribe(self):
        raise Exception('Unsupported operatioin')


class DataPoint(Generic[T]):
    def __init__(
        self, protocol: DataPointProtocol, validator: DataPointValidator
    ):
        self._protocol = protocol
        self._validator = validator

    def name(self) -> tuple[str, str]:
        return self._protocol.name()

    async def get_value_async(self) -> T:
        value = await self._protocol.get_val()
        if self._validator.validate(value):
            return value
        raise Exception(
            f'invalid value read from device, {value}, validator: {self._validator.data_type()}'
        )

    def get_value(self) -> T:
        return run(self.get_value_async())

    async def set_value_async(self, value: T):
        if self._validator.validate(value):
            return await self._protocol.set_val(value)
        raise Exception('invalid data to write to device')

    def set_value(self, value: T):
        return run(self.set_value_async(value))

    def subscribe(self, fn: Callable[[Any], None]):
        self._protocol.subscribe(fn)

    def unsubscribe(self):
        self._protocol.unsubscribe()

    def direction(self) -> DataDirectionProduct:
        return self._protocol.direction()

    def data_type(self) -> DataTypes:
        return self._validator.data_type()

    def describe(
        self,
    ) -> tuple[tuple[str, str], DataDirectionProduct, DataTypes]:
        return self.name(), self.direction(), self.data_type()

    def options(self) -> list[Any]:
        options = self._validator.options()
        if options is None:
            return []
        return options
