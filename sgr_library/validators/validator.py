from typing import Any

from sgr_library.api import DataPointValidator
from sgr_library.api.data_types import DataTypes
from sgrspecification.generic import EnumMapProduct


class UnsupportedValidator(DataPointValidator):
    def __init__(self, type: Any):
        self._type = type

    def validate(self, value: Any) -> bool:
        return False


class EnumValidator(DataPointValidator):
    def __init__(self, type: EnumMapProduct):
        self._type = type
        literals = {entry.literal for entry in type.enum_entry}
        ordinals = {entry.ordinal for entry in type.enum_entry}
        literals.union(ordinals)
        literals.discard(None)
        self._valid_entries: list[str] = literals

    def validate(self, value: Any) -> bool:
        return value in self._valid_entries

    def data_type(self):
        return DataTypes.ENUM

    def options(self) -> list[str] | None:
        return self._valid_entries


class IntValidator(DataPointValidator):

    def __init__(self, size: int, signed: bool = False):
        self._size = size
        if signed:
            self._lower_bound = -2 ** (self._size - 1)
            self._upper_bound = 2 ** (self._size - 1)
        else:
            self._lower_bound = 0
            self._upper_bound = 2 ** self._size - 1

    def validate(self, value: Any) -> bool:
        print(isinstance(value, int), self._lower_bound <= value <= self._upper_bound)
        return isinstance(value, int) and self._lower_bound <= value <= self._upper_bound

    def data_type(self):
        return DataTypes.INT


class FloatValidator(DataPointValidator):

    def __init__(self, size: int):
        self._size = size

    def validate(self, value: Any) -> bool:
        return isinstance(value, float) or isinstance(value,
                                                      int)  # added int here as the test sensor returns int and i have nothing else to test

    def data_type(self):
        return DataTypes.FLOAT


class StringValidator(DataPointValidator):

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def data_type(self):
        return DataTypes.STRING


class BooleanValidator(DataPointValidator):

    def validate(self, value: Any) -> bool:
        return isinstance(value, bool)

    def data_type(self):
        return DataTypes.BOOLEAN
