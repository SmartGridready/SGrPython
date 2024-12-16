from datetime import datetime
from typing import Any

from sgr_specification.v0.generic import EnumMapProduct

from sgr_commhandler.api import DataPointValidator
from sgr_commhandler.api.data_types import DataTypes

INT_SIZES: set[int] = {8, 16, 32, 64}
FLOAT_SIZES: set[int] = {32, 64}


class UnsupportedValidator(DataPointValidator):
    def validate(self, value: Any) -> bool:
        return False


class EnumValidator(DataPointValidator):
    def __init__(self, type: EnumMapProduct):
        if type and type.enum_entry:
            self._valid_ordinals: set[int] = {
                entry.ordinal
                for entry in type.enum_entry
                if entry.ordinal is not None
            }
            self._valid_literals: set[str] = {
                entry.literal
                for entry in type.enum_entry
                if entry.literal is not None
            }
            self._options: list[tuple[str, int]] = [
                (entry.literal, entry.ordinal)
                for entry in type.enum_entry
                if entry.ordinal is not None and entry.literal is not None
            ]
        else:
            self._valid_literals: set[str] = set()
            self._valid_ordinals: set[int] = set()
            self._options: list[tuple[str, int]] = []

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        return (isinstance(value, str) and value in self._valid_literals) or (
            isinstance(value, int) and value in self._valid_ordinals
        )

    def data_type(self) -> DataTypes:
        return DataTypes.ENUM

    def options(self) -> list[Any]:
        return self._options


class IntValidator(DataPointValidator):
    def __init__(self, size: int, signed: bool = True):
        self._size = size if size in INT_SIZES else next(iter(INT_SIZES))
        if signed:
            self._lower_bound = -(2 ** (self._size - 1))
            self._upper_bound = (2 ** (self._size - 1)) - 1
        else:
            # TODO verify that this even works with uint64
            self._lower_bound = 0
            self._upper_bound = (2**self._size) - 1

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, float):
            return self._lower_bound <= value <= self._upper_bound
        try:
            return self._lower_bound <= int(value) <= self._upper_bound
        except Exception:
            return False

    def data_type(self) -> DataTypes:
        return DataTypes.INT


class FloatValidator(DataPointValidator):
    def __init__(self, size: int):
        self._size = size if size in FLOAT_SIZES else next(iter(FLOAT_SIZES))

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, float):
            return True
        try:
            float(value)
            return True
        except Exception:
            return False

    def data_type(self) -> DataTypes:
        return DataTypes.FLOAT


class StringValidator(DataPointValidator):
    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return True
        try:
            str(value)
            return True
        except Exception:
            return False

    def data_type(self) -> DataTypes:
        return DataTypes.STRING


class BooleanValidator(DataPointValidator):
    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return True
        try:
            bool(value)
            return True
        except Exception:
            return False

    def data_type(self) -> DataTypes:
        return DataTypes.BOOLEAN


class BitmapValidator(DataPointValidator):
    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        return isinstance(value, dict)

    def data_type(self) -> DataTypes:
        return DataTypes.BITMAP


class DateTimeValidator(DataPointValidator):
    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        # TODO fully implement conversion
        return isinstance(value, datetime)

    def data_type(self) -> DataTypes:
        return DataTypes.DATE_TIME
