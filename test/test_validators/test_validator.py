from sgrspecification.generic import EnumEntryProductRecord, EnumMapProduct

from sgr_library.api.data_types import DataTypes
from sgr_library.validators.validator import (
    BooleanValidator,
    EnumValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
    UnsupportedValidator,
)


def test_unsupported_validator():
    validator = UnsupportedValidator({})
    assert not validator.validate(123)
    assert not validator.validate("test")
    assert not validator.validate(None)
    assert not validator.validate(True)
    assert not validator.validate(12.34)


def test_enum_validator():
    # Create enum entries
    entries = [
        EnumEntryProductRecord(literal="RED", ordinal=1),
        EnumEntryProductRecord(literal="GREEN", ordinal=2),
        EnumEntryProductRecord(literal="BLUE", ordinal=3),
    ]
    enum_type = EnumMapProduct(enum_entry=entries)
    validator = EnumValidator(type=enum_type)

    # Valid values
    assert validator.validate("RED")
    assert validator.validate("GREEN")
    assert validator.validate("BLUE")
    assert validator.validate(1)
    assert validator.validate(2)
    assert validator.validate(3)

    # Invalid values
    assert not validator.validate("YELLOW")
    assert not validator.validate(4)
    assert not validator.validate(None)
    assert not validator.validate(True)

    # Test data_type
    assert validator.data_type() == DataTypes.ENUM

    # Test options
    expected_options = ["RED", "GREEN", "BLUE", 1, 2, 3]
    assert set(validator.options()) == set(expected_options)


def test_int_validator_unsigned_8bit():
    validator = IntValidator(size=8, signed=False)
    assert validator.validate(0)
    assert validator.validate(255)
    assert not validator.validate(256)
    assert not validator.validate(-1)
    assert not validator.validate(12.34)
    assert not validator.validate("100")


def test_int_validator_signed_8bit():
    validator = IntValidator(size=8, signed=True)
    assert validator.validate(-128)
    assert validator.validate(127)
    assert not validator.validate(-129)
    assert not validator.validate(128)
    assert not validator.validate(12.34)
    assert not validator.validate("100")


def test_int_validator_data_type():
    validator = IntValidator(size=16, signed=True)
    assert validator.data_type() == DataTypes.INT


def test_float_validator():
    validator = FloatValidator(size=32)
    assert validator.validate(12.34)
    assert validator.validate(-56.78)
    assert validator.validate(0.0)
    assert validator.validate(100)  # Integers are acceptable
    assert validator.validate(-200)
    assert not validator.validate("100.0")
    assert not validator.validate(None)
    assert not validator.validate(True)


def test_float_validator_data_type():
    validator = FloatValidator(size=64)
    assert validator.data_type() == DataTypes.FLOAT


def test_string_validator():
    validator = StringValidator()
    assert validator.validate("hello")
    assert validator.validate("")
    assert not validator.validate(123)
    assert not validator.validate(12.34)
    assert not validator.validate(True)
    assert not validator.validate(None)


def test_string_validator_data_type():
    validator = StringValidator()
    assert validator.data_type() == DataTypes.STRING


def test_boolean_validator():
    validator = BooleanValidator()
    assert validator.validate(True)
    assert validator.validate(False)
    assert not validator.validate(1)
    assert not validator.validate(0)
    assert not validator.validate("True")
    assert not validator.validate(None)


def test_boolean_validator_data_type():
    validator = BooleanValidator()
    assert validator.data_type() == DataTypes.BOOLEAN
