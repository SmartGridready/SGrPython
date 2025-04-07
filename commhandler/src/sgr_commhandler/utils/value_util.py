import logging
from enum import Enum
from math import ceil, floor


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
