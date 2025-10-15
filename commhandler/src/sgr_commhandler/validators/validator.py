"""
Provides data type validators.
"""

from datetime import datetime
from typing import Any, Optional

from sgr_specification.v0.generic import EnumMapProduct

from sgr_commhandler.api.data_point_api import DataPointValidator
from sgr_commhandler.api.data_types import DataTypes

INT_SIZES: set[int] = {8, 16, 32, 64}
FLOAT_SIZES: set[int] = {32, 64}


class UnsupportedValidator(DataPointValidator):
    """
    Implements a default validator for all unsupported data types.
    """

    def __init__(self):
        super().__init__(DataTypes.UNDEFINED)

    def validate(self, value: Any) -> bool:
        return False


class EnumValidator(DataPointValidator):
    """
    Implements a validator for enumeration values.
    """

    def __init__(self, type: EnumMapProduct):
        super().__init__(DataTypes.ENUM)
        self._valid_literals: set[str] = set()
        self._valid_ordinals: set[int] = set()
        if type and type.enum_entry:
            self._options = list(map(lambda e: (e.literal, e.ordinal), type.enum_entry))
            for o in self._options:
                if o[0]:
                    self._valid_literals.add(o[0])
                if o[1]:
                    self._valid_ordinals.add(o[1])
        else:
            self._options: list[tuple[Optional[str], Optional[int]]] = []

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        return (isinstance(value, str) and value in self._valid_literals) or (
            isinstance(value, int) and value in self._valid_ordinals
        )

    def options(self) -> list[Any]:
        return self._options


class IntValidator(DataPointValidator):
    """
    Implements a validator for integer values.
    """

    def __init__(self, size: int, signed: bool = True):
        super().__init__(DataTypes.INT)
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


class FloatValidator(DataPointValidator):
    """
    Implements a validator for floating-point values.
    """

    def __init__(self, size: int):
        super().__init__(DataTypes.FLOAT)
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


class StringValidator(DataPointValidator):
    """
    Implements a validator for text strings.
    """

    def __init__(self):
        super().__init__(DataTypes.STRING)

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


class BooleanValidator(DataPointValidator):
    """
    Implements a validator for boolean values.
    """

    def __init__(self):
        super().__init__(DataTypes.BOOLEAN)

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


class BitmapValidator(DataPointValidator):
    """
    Implements a validator for bitmap values.
    """

    def __init__(self):
        super().__init__(DataTypes.BITMAP)

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        return isinstance(value, dict)


class DateTimeValidator(DataPointValidator):
    """
    Implements a validator for date/time values.
    """

    def __init__(self):
        super().__init__(DataTypes.DATE_TIME)

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        # TODO fully implement conversion
        return isinstance(value, datetime)


class JsonValidator(DataPointValidator):
    """
    Implements a validator for JSON values.
    """

    def __init__(self):
        super().__init__(DataTypes.JSON)

    def validate(self, value: Any) -> bool:
        # can be anything
        return value is not None
