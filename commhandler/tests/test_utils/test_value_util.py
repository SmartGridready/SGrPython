import pytest

from sgr_commhandler.utils import value_util

"""
Test conversion of values to the unit of a data point.
"""


@pytest.mark.parametrize(
    'value, expected',
    [(3000.0, 3.0), (3000, 3.0), ('3000', 3.0), (' 3000.5 ', 3.0005), (0, 0.0)],
)
def test_convert_to_dp_units_number(value, expected):
    converted = value_util.convert_to_dp_units(value, 0.001)

    assert isinstance(converted, float)
    assert converted == pytest.approx(expected)


@pytest.mark.parametrize('value', [None, True, False, 'n/a', '', [3000.0], {'power': 3000.0}])
def test_convert_to_dp_units_not_a_number(value):
    assert value_util.convert_to_dp_units(value, 0.001) == value


def test_convert_to_dp_units_without_factor():
    assert value_util.convert_to_dp_units(3000.0, None) == 3000.0
    assert value_util.convert_to_dp_units('3000', None) == '3000'
