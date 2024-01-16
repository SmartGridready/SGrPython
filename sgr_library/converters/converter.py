from typing import Any

from sgr_library.api import DataPointConverter
from sgr_library.api.data_point_api import T
from sgr_library.api.sub_set_units import SubSetUnits
from sgr_library.data_classes.generic import Units


class VoltDataPointConverter(DataPointConverter[int]):

    def __init__(self, unit: Units):
        self._unit = unit
        self._factor = 1
        match unit:
            case unit.MILLIVOLTS:
                self._factor = 0.001
            case unit.KILOVOLTS:
                self._factor = 1000
            case unit.MEGAVOLTS:
                self._factor = 1000_000

    def to_device(self, value: int) -> Any:
        return value / self._factor

    def from_device(self, value: Any) -> int:
        return value * self._factor

    def converted_unit(self) -> SubSetUnits:
        return SubSetUnits.VOLTS

class ReactiveEnergyConverter(DataPointConverter[int]):

    def __init__(self, unit: Units):
        self._unit = unit

    def to_device(self, value: T) -> Any:
        return value

    def from_device(self, value: Any) -> T:
        return value

    def converted_unit(self) -> SubSetUnits:
        pass


class PowerOverTimeConverter(DataPointConverter[int]):
    def __init__(self, unit: Units):
        self._unit = unit

    def to_device(self, value: T) -> Any:
        return value

    def from_device(self, value: Any) -> T:
        return value

    def converted_unit(self) -> SubSetUnits:
        pass


class CurrentConverter(DataPointConverter[int]):

    def __init__(self, unit: Units):
        self._unit = unit

    def to_device(self, value: T) -> Any:
        return value

    def from_device(self, value: Any) -> T:
        return value

    def converted_unit(self) -> SubSetUnits:
        pass


class PowerConverter(DataPointConverter[int]):

    def __init__(self, unit: Units):
        self._unit = unit

    def to_device(self, value: T) -> Any:
        return value

    def from_device(self, value: Any) -> T:
        return value

    def converted_unit(self) -> SubSetUnits:
        pass


class PercentConverter(DataPointConverter[int]):

    def __init__(self, unit: Units):
        self._unit = unit

    def to_device(self, value: T) -> Any:
        return value

    def from_device(self, value: Any) -> T:
        return value

    def converted_unit(self) -> SubSetUnits:
        pass


class UnsupportedConverter(DataPointConverter[Any]):

    def __init__(self, unit: Units):
        self._unit = unit

    def to_device(self, value: Any) -> Any:
        raise Exception(f"unsupported unit, {self._unit}")

    def from_device(self, value: Any) -> Any:
        raise Exception(f"unsupported unit, {self._unit}")

    def converted_unit(self) -> SubSetUnits:
        raise Exception(f"unsupported unit, {self._unit}")
