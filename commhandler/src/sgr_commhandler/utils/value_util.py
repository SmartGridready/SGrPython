"""
Provides data value manipulation functions.
"""

import logging
from enum import Enum
from math import ceil, floor
from typing import Any, Optional


logger = logging.getLogger(__name__)


class RoundingScheme(Enum):
    """
    Defines the kind of rounding method.
    """
    floor = "floor"
    ceil = "ceil"
    near = "Near"


def round_to_int(
    value: float, scheme: RoundingScheme = RoundingScheme.floor
) -> int:
    """
    Rounds a floating-point value to an integer, using a given rounding method.

    Parameters
    ----------
    value : float
        the floating-point value to round
    scheme : RoundingScheme
        the method of rounding, defaults to floor
    """
    if scheme == RoundingScheme.floor:
        return floor(value)
    elif scheme == RoundingScheme.ceil:
        return ceil(value)
    elif scheme == RoundingScheme.near:
        return round(value)
    else:
        logger.warning(f'tried rounding with a invalid scheme ({scheme}) using floor instead')
        return int(floor(value))


def convert_to_dp_units(value: Any, unit_conv_factor: Optional[float]) -> Any:
    """
    Converts a value read from a device to the unit of the data point.

    Parameters
    ----------
    value : Any
        the value read from the device
    unit_conv_factor : Optional[float]
        the unit conversion multiplicator of the data point, if it has one

    Returns
    -------
    Any
        the value multiplied by the factor, as float, if it is a number or a numeric string;
        otherwise (no factor, boolean, None, JSON object, text) the value as it is
    """
    if unit_conv_factor is None or isinstance(value, bool):
        return value
    try:
        return float(value) * unit_conv_factor
    except (TypeError, ValueError):
        return value
