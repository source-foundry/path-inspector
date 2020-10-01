import argparse
import os
import sys

import pytest

from pathins.direction import direction_run

TESTFONT_PATH_1 = os.path.join(
    "tests", "testfiles", "fonts", "NotoSans-Regular.subset1.ttf"
)

# instantiate a parser for unit tests in this module
parser = argparse.ArgumentParser()
parser.add_argument("--nocolor", action="store_true", help="no ANSI color")
parser.add_argument("fontpath", type=str, help="font file path")
parser.add_argument(
    "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
)


def test_direction_run_error_invalid_path(capsys):
    test_path = os.path.join("bogus", "path.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        direction_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_direction_run_error_non_font_path(capsys):
    test_path = os.path.join("tests", "testfiles", "text", "test.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        direction_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a TTF format font" in captured.err


def test_direction_run_fail_invalid_glyphname(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "bogus"])
    with pytest.raises(SystemExit) as e:
        direction_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "Failed to open glyph" in captured.err


def test_path_run_single_glyph_non_composite_no_contours_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, ".notdef"])
    direction_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ \x1b[1;36m.notdef\x1b[0m ]: no contours" in captured.out


def test_path_run_single_glyph_non_composite_no_contours_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, ".notdef"])
    direction_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ .notdef ]: no contours" in captured.out


def test_path_run_single_glyph_non_composite_clockwise_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "A"])
    direction_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ \x1b[1;36mA\x1b[0m ]: clockwise" in captured.out


def test_path_run_single_glyph_non_composite_clockwise_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "A"])
    direction_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ A ]: clockwise" in captured.out


def test_path_run_single_glyph_composite_counter_clockwise_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "uni2E2E"])
    direction_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ \x1b[1;36muni2E2E\x1b[0m ]: counter-clockwise" in captured.out
    assert "with component 'question' transform: [[-1.0, 0], [0, 1.0]]" in captured.out


def test_path_run_single_glyph_composite_counter_clockwise_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "uni2E2E"])
    direction_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert captured.out == (
        "[ uni2E2E ]: counter-clockwise\n"
        "          with component 'question' transform: [[-1.0, 0], [0, 1.0]]\n"
    )
