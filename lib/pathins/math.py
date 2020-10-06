import math
from typing import Tuple

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Point math
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~


def round_point(pt: float) -> int:
    """
    Round float value towards +Infinity.

    This function rounds values with the approach:
      for fractional values of 0.5 and higher, take the next higher integer;
      for other fractional values, truncate.
    This means that 7.5 rounds to 8, whereas -7.5
    rounds to -7.

    Re-implementation of the fonttools.misc.fixedTools.otRound
    function for rounding of float values.

    See https://github.com/fonttools/fonttools/issues/1248#issuecomment-383198166
    for discussion of the rationale for this rounding approach.
    """
    return int(math.floor(pt + 0.5))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Cartesian coordinate math
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~


def linear_distance_between_coordinates(
    coord1: Tuple[int, int], coord2: Tuple[int, int]
) -> float:
    """
    Returns the linear distance between two sets of
    Cartesian coordinate values.
    """
    x1, y1 = coord1
    x2, y2 = coord2
    x_diff_squared = (x2 - x1) ** 2
    y_diff_squared = (y2 - y1) ** 2
    return math.sqrt(x_diff_squared + y_diff_squared)


def midpoint_between_coordinates(
    coord1: Tuple[int, int], coord2: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Returns (x, y) midpoint between two Cartesian coordinates
    where coord1 and coord2 are tuples of x, y integer
    values.

    See https://github.com/fonttools/fonttools/issues/1248#issuecomment-383198166
    for discussion of the rationale for this rounding approach.
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return round_point((x1 + x2) / 2), round_point((y1 + y2) / 2)
