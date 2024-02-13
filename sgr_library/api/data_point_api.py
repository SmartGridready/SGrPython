from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

from sgr_library.api.data_types import DataTypes
from sgr_library.api.sub_set_units import SubSetUnits
from sgr_library.data_classes.generic import DataDirection

T = TypeVar('T')


class DataPointConverter(ABC, Generic[T]):

    @abstractmethod
    def to_device(self, value: T) -> Any:
        pass

    @abstractmethod
    def from_device(self, value: Any) -> T:
        pass

    @abstractmethod
    def converted_unit(self) -> SubSetUnits:
        pass


class DataPointValidator(ABC):

    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass

    @abstractmethod
    def data_type(self):
        pass


class DataPointProtocol(ABC):

    @abstractmethod
    async def write(self, data: Any):
        pass

    @abstractmethod
    async def read(self) -> Any:
        pass

    @abstractmethod
    def name(self) -> tuple[str, str]:
        pass

    @abstractmethod
    def direction(self) -> DataDirection:
        pass


class DataPoint(Generic[T]):

    def __init__(self, protocol: DataPointProtocol, converter: DataPointConverter[T], validator: DataPointValidator):
        self._protocol = protocol
        self._converter = converter
        self._validator = validator

    def name(self) -> tuple[str, str]:
        return self._protocol.name()

    async def read(self) -> T:
        value = await self._protocol.read()
        if self._validator.validate(value):
            return self._converter.from_device(value)
        raise Exception(f"invalid value read from device, {value}, validator: {self._validator.data_type()}")

    async def write(self, data: T):
        value = self._converter.to_device(data)
        if self._validator.validate(value):
            await self._protocol.write(value)
        raise Exception("invalid data to write to device")

    def unit(self) -> SubSetUnits:
        return self._converter.converted_unit()

    def direction(self) -> DataDirection:
        return self._protocol.direction()

    def data_type(self) -> DataTypes:
        return self._validator.data_type()

    def describe(self) -> tuple[tuple[str, str], DataDirection, DataTypes]:
        return self.name(), self.direction(), self.data_type()
