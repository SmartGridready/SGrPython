from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Tuple

from sgr_library.api.data_types import DataTypes
from sgrspecification.generic import DataDirectionProduct
from asyncio import run

T = TypeVar('T')

class DataPointValidator(ABC):

    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass

    @abstractmethod
    def data_type(self) -> DataTypes:
        pass

    def options(self) -> list[str] | None:
        return None


class DataPointProtocol(ABC):

    @abstractmethod
    async def write(self, data: Any):
        pass

    @abstractmethod
    async def read(self) -> Any:
        pass

    @abstractmethod
    def name(self) -> Tuple[str, str]:
        pass

    @abstractmethod
    def direction(self) -> DataDirectionProduct:
        pass


class DataPoint(Generic[T]):

    def __init__(self, protocol: DataPointProtocol, validator: DataPointValidator):
        self._protocol = protocol
        self._validator = validator

    def name(self) -> Tuple[str, str]:
        return self._protocol.name()

    async def get_value_async(self) -> T:
        value = await self._protocol.read()
        if self._validator.validate(value):
            return value
        raise Exception(f"invalid value read from device, {value}, validator: {self._validator.data_type()}")

    def get_value(self) -> T:
        return run(self.get_value_async())

    async def set_value_async(self, data: T):
        if self._validator.validate(data):
            return await self._protocol.write(data)
        raise Exception("invalid data to write to device")

    def set_value(self, data: T):
        return run(self.set_value_async(data=data))

    def direction(self) -> DataDirectionProduct:
        return self._protocol.direction()

    def data_type(self) -> DataTypes:
        return self._validator.data_type()

    def describe(self) -> Tuple[Tuple[str, str], DataDirectionProduct, DataTypes]:
        return self.name(), self.direction(), self.data_type()

    def options(self) -> list[str]:
        options = self._validator.options()
        if options == None:
            return []
        return options
