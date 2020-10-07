import pytest

from pathins.datastructures import Coordinate


def test_coordinate_instantiation_default():
    c = Coordinate(1, 2)
    assert c.x == 1
    assert c.y == 2
    assert c.oncurve is False
    assert c.implied is False
    assert c.startpoint is False
    assert c.endpoint is False
    assert c.coord_next is None
    assert c.coord_previous is None


def test_coordinate_equality():
    a = Coordinate(1, 2)
    b = Coordinate(1, 2)
    assert a == b


def test_coordinate_inequality():
    a = Coordinate(1, 2)
    b = Coordinate(1, 3)
    c = Coordinate(1, 2, startpoint=True)
    d = Coordinate(1, 2, endpoint=True)
    e = Coordinate(1, 2, implied=True)

    assert a != b
    assert a != c
    assert a != d
    assert a != e


def test_coordinate_set_coord_next_method():
    c = Coordinate(1, 2)
    c.set_coord_next(Coordinate(3, 4))
    assert c.coord_next == Coordinate(3, 4)
    assert c.coord_previous is None


def test_coordinate_set_coord_previous_method():
    c = Coordinate(1, 2)
    c.set_coord_previous(Coordinate(3, 4))
    assert c.coord_previous == Coordinate(3, 4)
    assert c.coord_next is None


def test_coordinate_str_method():
    c = Coordinate(1, 2)

    assert (
        str(c)
        == "Coordinate< (1,2) oncurve: False, startpoint: False, endpoint: False, implied: False >"
    )
    assert (
        c.__str__()
        == "Coordinate< (1,2) oncurve: False, startpoint: False, endpoint: False, implied: False >"
    )
    c.x = 3
    assert (
        c.__str__()
        == "Coordinate< (3,2) oncurve: False, startpoint: False, endpoint: False, implied: False >"
    )
    c.oncurve = True
    assert (
        c.__str__()
        == "Coordinate< (3,2) oncurve: True, startpoint: False, endpoint: False, implied: False >"
    )
    c.startpoint = True
    assert (
        c.__str__()
        == "Coordinate< (3,2) oncurve: True, startpoint: True, endpoint: False, implied: False >"
    )
    c.endpoint = True
    assert (
        c.__str__()
        == "Coordinate< (3,2) oncurve: True, startpoint: True, endpoint: True, implied: False >"
    )
    c.implied = True
    assert (
        c.__str__()
        == "Coordinate< (3,2) oncurve: True, startpoint: True, endpoint: True, implied: True >"
    )


def test_coordinate_repr_method():
    c = Coordinate(1, 2)
    assert (
        c.__repr__()
        == "Coordinate< (1,2) oncurve: False, startpoint: False, endpoint: False, implied: False >"
    )
    c.x = 3
    assert (
        c.__repr__()
        == "Coordinate< (3,2) oncurve: False, startpoint: False, endpoint: False, implied: False >"
    )
    c.oncurve = True
    assert (
        c.__repr__()
        == "Coordinate< (3,2) oncurve: True, startpoint: False, endpoint: False, implied: False >"
    )
    c.startpoint = True
    assert (
        c.__repr__()
        == "Coordinate< (3,2) oncurve: True, startpoint: True, endpoint: False, implied: False >"
    )
    c.endpoint = True
    assert (
        c.__repr__()
        == "Coordinate< (3,2) oncurve: True, startpoint: True, endpoint: True, implied: False >"
    )
    c.implied = True
    assert (
        c.__repr__()
        == "Coordinate< (3,2) oncurve: True, startpoint: True, endpoint: True, implied: True >"
    )
