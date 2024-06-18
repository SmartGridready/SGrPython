from sgr_library.api import DataPointValidator
from sgrspecification.generic import DataTypeProduct
from sgr_library.validators.validator import IntValidator, EnumValidator, FloatValidator, StringValidator, \
    BooleanValidator


def build_validator(type: DataTypeProduct) -> DataPointValidator:
    if type.int8:
        return IntValidator(8)
    elif type.int16:
        return IntValidator(16)
    elif type.int32:
        return IntValidator(32)
    elif type.int64:
        return IntValidator(64)
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
        raise Exception("unsupported validator")  # return BitmapValidator(type.bitmap)
    elif type.date_time:
        raise Exception("unsupported validator")
    raise Exception("unsupported validator")
