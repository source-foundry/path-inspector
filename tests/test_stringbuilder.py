import os

import pytest

import pathins.stringbuilder
from pathins.datastructures import Coordinate


def test_bold_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.bold_text("TEST")
    assert res == "\033[1mTEST\033[0m"


def test_bold_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.bold_text("TEST", nocolor=True)
    assert res == "TEST"


def test_cyan_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_text("TEST")
    assert res == "\033[36mTEST\033[0m"


def test_cyan_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_text("TEST", nocolor=True)
    assert res == "TEST"


def test_cyan_bright_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_bright_text("TEST")
    assert res == "\033[1;96mTEST\033[0m"


def test_cyan_bright_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_bright_text("TEST", nocolor=True)
    assert res == "TEST"


def test_green_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.green_text("TEST")
    assert res == "\033[32mTEST\033[0m"


def test_green_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.green_text("TEST", nocolor=True)
    assert res == "TEST"


def test_red_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.red_text("TEST")
    assert res == "\033[31mTEST\033[0m"


def test_red_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.red_text("TEST", nocolor=True)
    assert res == "TEST"


def test_report_header(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.report_header("TEST")
    assert res == f"-----{os.linesep}\033[1;96mTEST\033[0m{os.linesep}-----"


def test_report_header_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.report_header("TEST", nocolor=True)
    assert res == f"-----{os.linesep}TEST{os.linesep}-----"


# def test_overlap_result_pass_default(monkeypatch):
#     # mock tty
#     def mock_isatty():
#         return True

#     # apply the monkeypatch for sys.stdout.isatty()
#     monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

#     res = pathins.stringbuilder.overlap_result("TEST", test_pass=True)
#     assert res == "[ \x1b[31mTEST\x1b[0m ]: Yes"


# def test_overlap_result_pass_nocolor(monkeypatch):
#     # mock tty
#     def mock_isatty():
#         return True

#     # apply the monkeypatch for sys.stdout.isatty()
#     monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

#     res = pathins.stringbuilder.overlap_result("TEST", test_pass=True, nocolor=True)
#     assert res == "[ TEST ]: Yes"


def test_direction_result_no_contours_default(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.direction_result("TEST", True, 0, [], nocolor=False)
    assert res == "[ \033[1;96mTEST\033[0m ]: no contours"


def test_direction_result_no_contours_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.direction_result("TEST", True, 0, [], nocolor=True)
    assert res == "[ TEST ]: no contours"


def test_direction_result_clockwise_with_component_transform(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.direction_result(
        "TEST", True, 2, [("A", [[1.0, 0], [0, 1.0]])], nocolor=False
    )
    assert res == (
        f"[ \033[1;96mTEST\033[0m ]: clockwise{os.linesep}"
        f"          with component 'A' transform: [[1.0, 0], [0, 1.0]]"
    )


def test_direction_result_clockwise_with_two_components(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.direction_result(
        "TEST",
        True,
        2,
        [("A", [[1.0, 0], [0, 1.0]]), ("B", [[1.0, 0], [0, 1.0]])],
        nocolor=False,
    )
    assert res == (
        f"[ \033[1;96mTEST\033[0m ]: clockwise{os.linesep}"
        f"          with component 'A' transform: [[1.0, 0], [0, 1.0]]{os.linesep}"
        f"          with component 'B' transform: [[1.0, 0], [0, 1.0]]"
    )


def test_direction_result_counterclockwise_with_component_transform(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.direction_result(
        "TEST", False, 2, [("A", [[1.0, 0], [0, 1.0]])], nocolor=False
    )
    assert res == (
        f"[ \033[1;96mTEST\033[0m ]: counter-clockwise{os.linesep}"
        f"          with component 'A' transform: [[1.0, 0], [0, 1.0]]"
    )


def test_direction_result_counterclockwise_with_two_components(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.direction_result(
        "TEST",
        False,
        2,
        [("A", [[1.0, 0], [0, 1.0]]), ("B", [[1.0, 0], [0, 1.0]])],
        nocolor=False,
    )
    assert res == (
        f"[ \033[1;96mTEST\033[0m ]: counter-clockwise{os.linesep}"
        f"          with component 'A' transform: [[1.0, 0], [0, 1.0]]{os.linesep}"
        f"          with component 'B' transform: [[1.0, 0], [0, 1.0]]"
    )


def test_segment_line_default(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, True, False, False, False)
    res = pathins.stringbuilder.segment_line(coord1, coord2, 1.0, nocolor=False)
    assert res == "(0,0) (1,1): \033[1;96mLINE\033[0m 1.00 units"


def test_segment_line_with_coord1_startpoint_color(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, True, False, False)
    coord2 = Coordinate(1, 1, True, False, False, False)
    res = pathins.stringbuilder.segment_line(coord1, coord2, 1.0, nocolor=False)
    assert res == "\033[32m(0,0)\033[0m (1,1): \033[1;96mLINE\033[0m 1.00 units"


def test_segment_line_with_coord2_startpoint_color(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, True, True, False, False)
    res = pathins.stringbuilder.segment_line(coord1, coord2, 1.0, nocolor=False)
    assert res == "(0,0) \033[32m(1,1)\033[0m: \033[1;96mLINE\033[0m 1.00 units"


def test_segment_line_with_endpoint_color(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, True, False)
    coord2 = Coordinate(1, 1, True, False, False, False)
    res = pathins.stringbuilder.segment_line(coord1, coord2, 1.0, nocolor=False)
    assert res == "\033[31m(0,0)\033[0m (1,1): \033[1;96mLINE\033[0m 1.00 units"


def test_segment_line_with_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, True, False)
    coord2 = Coordinate(1, 1, True, False, False, False)
    res = pathins.stringbuilder.segment_line(coord1, coord2, 1.0, nocolor=True)
    assert res == "(0,0) (1,1): LINE 1.00 units"


def test_segment_quadratic_curve_default(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, False, False, False, False)
    coord3 = Coordinate(2, 2, True, False, False, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=False
    )
    assert res == "(0,0) (1,1) (2,2): \033[1;96mQCURVE\033[0m 1.00 units"


def test_segment_quadratic_curve_coord1_startpoint(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, True, False, False)
    coord2 = Coordinate(1, 1, False, False, False, False)
    coord3 = Coordinate(2, 2, True, False, False, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=False
    )
    assert res == "\033[32m(0,0)\033[0m (1,1) (2,2): \033[1;96mQCURVE\033[0m 1.00 units"


def test_segment_quadratic_curve_coord3_startpoint(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, False, False, False, False)
    coord3 = Coordinate(2, 2, True, True, False, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=False
    )
    assert res == "(0,0) (1,1) \033[32m(2,2)\033[0m: \033[1;96mQCURVE\033[0m 1.00 units"


def test_segment_quadratic_curve_coord1_endpoint(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, True, False)
    coord2 = Coordinate(1, 1, False, False, False, False)
    coord3 = Coordinate(2, 2, True, False, False, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=False
    )
    assert res == "\033[31m(0,0)\033[0m (1,1) (2,2): \033[1;96mQCURVE\033[0m 1.00 units"


def test_segment_quadratic_curve_coord3_endpoint(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, False, False, False, False)
    coord3 = Coordinate(2, 2, True, False, True, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=False
    )
    assert res == "(0,0) (1,1) \033[31m(2,2)\033[0m: \033[1;96mQCURVE\033[0m 1.00 units"


def test_segment_quadratic_curve_coord2_coord3_endpoint_startpoint(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, False, False, True, False)
    coord3 = Coordinate(2, 2, True, True, False, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=False
    )
    assert (
        res
        == "(0,0) \033[31m(1,1)\033[0m \033[32m(2,2)\033[0m: \033[1;96mQCURVE\033[0m 1.00 units"
    )


def test_segment_quadratic_curve_nocolor_default(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    coord1 = Coordinate(0, 0, True, False, False, False)
    coord2 = Coordinate(1, 1, False, False, True, False)
    coord3 = Coordinate(2, 2, True, True, False, False)
    res = pathins.stringbuilder.segment_quadratic_curve(
        coord1, coord2, coord3, 1.0, nocolor=True
    )
    assert res == "(0,0) (1,1) (2,2): QCURVE 1.00 units"
