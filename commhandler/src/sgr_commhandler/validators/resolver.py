from typing import Optional

from sgr_specification.v0.generic import DataTypeProduct

from sgr_commhandler.api.data_point_api import DataPointValidator
from sgr_commhandler.validators.validator import (
    BitmapValidator,
    BooleanValidator,
    DateTimeValidator,
    EnumValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
    JsonValidator
)


def build_validator(type: Optional[DataTypeProduct]) -> DataPointValidator:
    """
    Builds a data point validator from a data type specification.

    Parameters
    ----------
    type : Optional[DataTypeProduct]
        the data type specification

    Returns
    -------
    DataPointValidator
        a data point validator

    Raises
    ------
    Exception
        when data type has no supported validator
    """
    if type is None:
        raise Exception("Missing datatype")
    if type.int8 is not None:
        return IntValidator(8, signed=True)
    elif type.int16 is not None:
        return IntValidator(16, signed=True)
    elif type.int32 is not None:
        return IntValidator(32, signed=True)
    elif type.int64 is not None:
        return IntValidator(64, signed=True)
    elif type.enum is not None:
        return EnumValidator(type.enum)
    elif type.int8_u is not None:
        return IntValidator(8, signed=False)
    elif type.int16_u is not None:
        return IntValidator(16, signed=False)
    elif type.int32_u is not None:
        return IntValidator(32, signed=False)
    elif type.int64_u is not None:
        return IntValidator(64, signed=False)
    elif type.float32 is not None:
        return FloatValidator(32)
    elif type.float64 is not None:
        return FloatValidator(64)
    elif type.string is not None:
        return StringValidator()
    elif type.boolean is not None:
        return BooleanValidator()
    elif type.bitmap is not None:
        return BitmapValidator()
    elif type.date_time is not None:
        return DateTimeValidator()
    elif type.json is not None:
        return JsonValidator()
    raise Exception(f'unsupported validator: {type}')
