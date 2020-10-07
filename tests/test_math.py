import math

import pathins.math
import pytest

#
# pathins.math.round_point
#


def test_round_point():
    tests = [
        [0.0, 0],
        [1.4, 1],
        [1.6, 2],
        [-1.4, -1],
        [-1.6, -2],
        [1.5, 2],  # note behavior here
        [-1.5, -1],  # note behavior here
    ]

    for test in tests:
        assert pathins.math.round_point(test[0]) == test[1]


#
# pathins.math.midpoint_between_coordinates
#


def test_linear_distance_between_coordinates():
    tests = (
        [(0, 0), (40, 0), 40],
        [(0, 0), (0, 40), 40],
        [(0, 0), (10, 10), 14.1421356],
        [(0, 0), (0, 0), 0],
        [(0, 0), (-40, 0), 40],
        [(0, 0), (-10, -10), 14.1421356],
    )

    for test in tests:
        test_result = pathins.math.linear_distance_between_coordinates(test[0], test[1])
        assert math.isclose(test_result, test[2], rel_tol=1e-3) is True


#
# pathins.math.midpoint_between_coordinates
#


def test_midpoint_between_coordinates():
    # test list definitions: [coord1, coord2, expected midpoint]
    tests = [
        [(0, 0), (40, 0), (20, 0)],
        [(0, 0), (0, 40), (0, 20)],
        [(0, 0), (0, -40), (0, -20)],
        [(0, 0), (-40, 0), (-20, 0)],
        [(15, 0), (0, 0), (8, 0)],  # rounds towards +Infinity
        [(0, 15), (0, 0), (0, 8)],  # rounds towards +Infinity
        [(-15, -15), (0, 0), (-7, -7)],  # rounds towards +Infinity
    ]

    for test in tests:
        assert pathins.math.midpoint_between_coordinates(test[0], test[1]) == test[2]
