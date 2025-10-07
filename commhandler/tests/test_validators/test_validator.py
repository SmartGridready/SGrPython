import json
from datetime import datetime

from sgr_specification.v0.generic import EnumEntryProductRecord, EnumMapProduct

from sgr_commhandler.api.data_types import DataTypes
from sgr_commhandler.validators.validator import (
    BitmapValidator,
    BooleanValidator,
    DateTimeValidator,
    EnumValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
    UnsupportedValidator,
    JsonValidator
)

"""
Test Validators.

Notes:

Boolean values can be converted from/to int and float values:
- True == (i <> 0) or (f <> 0.0)
- False == (i == 0) or (f == 0.0)
"""


def test_unsupported_validator():
    validator = UnsupportedValidator()

    # Data type
    assert validator.data_type() == DataTypes.UNDEFINED

    # Invalid values
    assert not validator.validate(123)
    assert not validator.validate('test')
    assert not validator.validate(12.34)
    assert not validator.validate(True)
    assert not validator.validate(False)
    assert not validator.validate(None)


def test_enum_validator():
    # Create enum entries
    entries = [
        EnumEntryProductRecord(literal='RED', ordinal=1),
        EnumEntryProductRecord(literal='GREEN', ordinal=2),
        EnumEntryProductRecord(literal='BLUE', ordinal=3),
    ]
    enum_type = EnumMapProduct(enum_entry=entries)
    validator = EnumValidator(type=enum_type)

    # Data type
    assert validator.data_type() == DataTypes.ENUM

    # Valid values
    assert validator.validate('RED')
    assert validator.validate('GREEN')
    assert validator.validate('BLUE')
    assert validator.validate(1)
    assert validator.validate(2)
    assert validator.validate(3)
    assert validator.validate(True)

    # Invalid values
    assert not validator.validate('YELLOW')
    assert not validator.validate(4)
    assert not validator.validate(False)
    assert not validator.validate(None)

    # Test options
    expected_options = [('RED', 1), ('GREEN', 2), ('BLUE', 3)]
    assert set(validator.options()) == set(expected_options)


def test_int_validator_unsigned_8bit():
    validator = IntValidator(size=8, signed=False)

    # Data type
    assert validator.data_type() == DataTypes.INT

    # Valid values
    assert validator.validate(0)
    assert validator.validate(255)
    assert validator.validate('255')
    assert validator.validate(12.34)
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(256)
    assert not validator.validate(-1)
    assert not validator.validate(-12.34)
    assert not validator.validate(None)


def test_int_validator_signed_8bit():
    validator = IntValidator(size=8, signed=True)

    # Data type
    assert validator.data_type() == DataTypes.INT

    # Valid values
    assert validator.validate(-128)
    assert validator.validate(127)
    assert validator.validate('127')
    assert validator.validate(12.34)
    assert validator.validate(-12.34)
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(129.34)
    assert not validator.validate(-129.34)
    assert not validator.validate(-129)
    assert not validator.validate(128)
    assert not validator.validate(None)


def test_int_validator_unsigned_16bit():
    validator = IntValidator(size=16, signed=False)

    # Data type
    assert validator.data_type() == DataTypes.INT

    # Valid values
    assert validator.validate(0)
    assert validator.validate(65535)
    assert validator.validate('65535')
    assert validator.validate(12.34)
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(65536)
    assert not validator.validate(-1)
    assert not validator.validate(-12.34)
    assert not validator.validate(None)


def test_int_validator_signed_16bit():
    validator = IntValidator(size=16, signed=True)

    # Data type
    assert validator.data_type() == DataTypes.INT

    # Valid values
    assert validator.validate(-32768)
    assert validator.validate(32767)
    assert validator.validate('32767')
    assert validator.validate(12.34)
    assert validator.validate(-12.34)
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(-32769)
    assert not validator.validate(32768)
    assert not validator.validate(None)


def test_float_validator_32bit():
    validator = FloatValidator(size=32)

    # Data type
    assert validator.data_type() == DataTypes.FLOAT

    # Valid values
    assert validator.validate(12.34)
    assert validator.validate(-56.78)
    assert validator.validate(0.0)
    assert validator.validate(100)
    assert validator.validate(-200)
    assert validator.validate('100.0')
    assert validator.validate('-100')
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(None)


def test_float_validator_64bit():
    validator = FloatValidator(size=64)

    # Data type
    assert validator.data_type() == DataTypes.FLOAT

    # Valid values
    assert validator.validate(12.34)
    assert validator.validate(-56.78)
    assert validator.validate(0.0)
    assert validator.validate(100)
    assert validator.validate(-200)
    assert validator.validate('100.0')
    assert validator.validate('-100')
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(None)


def test_string_validator():
    validator = StringValidator()

    # Data type
    assert validator.data_type() == DataTypes.STRING

    # Valid values
    assert validator.validate('hello')
    assert validator.validate('')
    assert validator.validate(123)
    assert validator.validate(12.34)
    assert validator.validate(True)
    assert validator.validate(False)

    # Invalid values
    assert not validator.validate(None)


def test_boolean_validator():
    validator = BooleanValidator()

    # Data type
    assert validator.data_type() == DataTypes.BOOLEAN

    # Valid values
    assert validator.validate(True)
    assert validator.validate(False)
    assert validator.validate('True')
    assert validator.validate('False')
    assert validator.validate(1)
    assert validator.validate(0)

    # Invalid values
    assert not validator.validate(None)


def test_bitmap_validator():
    test_value: dict = {'name1': True, 'name2': False}

    validator = BitmapValidator()

    # Data type
    assert validator.data_type() == DataTypes.BITMAP

    # Valid values
    assert validator.validate(test_value)

    # Invalid values
    assert not validator.validate(True)
    assert not validator.validate(False)
    assert not validator.validate('True')
    assert not validator.validate('False')
    assert not validator.validate(1)
    assert not validator.validate(0)
    assert not validator.validate(None)


def test_datetime_validator():
    test_value = datetime.now()

    validator = DateTimeValidator()

    # Data type
    assert validator.data_type() == DataTypes.DATE_TIME

    # Valid values
    assert validator.validate(test_value)

    # Invalid values
    assert not validator.validate(True)
    assert not validator.validate(False)
    assert not validator.validate('True')
    assert not validator.validate('False')
    assert not validator.validate(1)
    assert not validator.validate(0)
    assert not validator.validate(None)


def test_json_validator():
    test_value = json.loads('{"textParam":"text","intParam":1234}')

    validator = JsonValidator()

    # Data type
    assert validator.data_type() == DataTypes.JSON

    # Valid values
    assert validator.validate(test_value)

    # Invalid values
    assert not validator.validate(None)
