from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

from sgr_library.api.data_types import DataTypes
from sgr_library.api.sub_set_units import SubSetUnits
from sgr_library.generated.generic import DataDirectionProduct

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
    def name(self) -> tuple[str, str]:
        pass

    @abstractmethod
    def direction(self) -> DataDirectionProduct:
        pass


class DataPoint(Generic[T]):

    def __init__(self, protocol: DataPointProtocol, validator: DataPointValidator):
        self._protocol = protocol
        self._validator = validator

    def name(self) -> tuple[str, str]:
        return self._protocol.name()

    async def read(self) -> T:
        value = await self._protocol.read()

        if self._validator.validate(value):
            return value
        raise Exception(f"invalid value read from device, {value}, validator: {self._validator.data_type()}")

    async def write(self, data: T):
        if self._validator.validate(data):
            return await self._protocol.write(data)
        raise Exception("invalid data to write to device")

    def direction(self) -> DataDirectionProduct:
        return self._protocol.direction()

    def data_type(self) -> DataTypes:
        return self._validator.data_type()

    def describe(self) -> tuple[tuple[str, str], DataDirectionProduct, DataTypes]:
        return self.name(), self.direction(), self.data_type()

    def options(self) -> list[str]:
        options = self._validator.options()
        if options == None:
            return []
        return options
