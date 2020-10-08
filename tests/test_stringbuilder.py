import os

import pytest

import pathins.stringbuilder


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
