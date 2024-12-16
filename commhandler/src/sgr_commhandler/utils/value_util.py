from enum import Enum
from math import ceil, floor


class RoundingScheme(Enum):
    floor = "floor"
    ceil = "ceil"
    near = "Near"


def round_to_int(
    value: float, scheme: RoundingScheme = RoundingScheme.floor
) -> int:
    if scheme == RoundingScheme.floor:
        return floor(value)
    elif scheme == RoundingScheme.ceil:
        return ceil(value)
    elif scheme == RoundingScheme.near:
        return round(value)
    else:
        print(
            "tried rounding with a invalid scheme (%s) using floor instead",
            scheme,
        )
        return int(floor(value))
