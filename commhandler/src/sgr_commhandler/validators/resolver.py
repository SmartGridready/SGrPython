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
    if type.int8:
        return IntValidator(8, signed=True)
    elif type.int16:
        return IntValidator(16, signed=True)
    elif type.int32:
        return IntValidator(32, signed=True)
    elif type.int64:
        return IntValidator(64, signed=True)
    elif type.enum:
        return EnumValidator(type.enum)
    elif type.int8_u:
        return IntValidator(8, signed=False)
    elif type.int16_u:
        return IntValidator(16, signed=False)
    elif type.int32_u:
        return IntValidator(32, signed=False)
    elif type.int64_u:
        return IntValidator(64, signed=False)
    elif type.float32:
        return FloatValidator(32)
    elif type.float64:
        return FloatValidator(64)
    elif type.string:
        return StringValidator()
    elif type.boolean:
        return BooleanValidator()
    elif type.bitmap:
        return BitmapValidator()
    elif type.date_time:
        return DateTimeValidator()
    elif type.json:
        return JsonValidator()
    raise Exception("unsupported validator")
