import argparse
import os
import sys

import pytest
from pathins.path import path_run
import pathins.stringbuilder

TESTFONT_PATH_1 = os.path.join("tests", "testfiles", "fonts", "RobotoMono-subset1.ttf")

# instantiate a parser for unit tests in this module
parser = argparse.ArgumentParser()
parser.add_argument("--nocolor", action="store_true", help="no ANSI color")
parser.add_argument("fontpath", type=str, help="font file path")
parser.add_argument(
    "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
)


def test_path_run_error_invalid_path(capsys):
    test_path = os.path.join("bogus", "path.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        path_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_path_run_error_non_font_path(capsys):
    test_path = os.path.join("tests", "testfiles", "text", "test.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        path_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a TTF format font" in captured.err


def test_path_run_fail_invalid_glyphname(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "bogus"])
    with pytest.raises(SystemExit) as e:
        path_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "Failed to open glyph" in captured.err


def test_path_run_single_glyph_non_composite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "A"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;96m'A' path\x1b[0m" in captured.out
    assert "path.moveTo(869, 377)" in captured.out


def test_path_run_single_glyph_non_composite_nocolor_with_option(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "A"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above and ANSI color should be off
    # due to command line flag
    assert "\x1b[1;96m'A' path\x1b[0m" not in captured.out
    assert "'A' path" in captured.out
    assert "path.moveTo(869, 377)" in captured.out


def test_path_run_single_glyph_non_composite_nocolor_when_not_tty(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "A"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is not mocked in this test and there should be no
    # color in non-tty test setting
    assert "\x1b[1;96m'A' path\x1b[0m" not in captured.out
    assert "'A' path" in captured.out
    assert "path.moveTo(869, 377)" in captured.out


def test_path_run_single_glyph_composite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "Scedilla"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;96m'Scedilla' path\x1b[0m" in captured.out
    assert "path.quadTo(728, -66, 699, -61)" in captured.out


def test_path_run_single_glyph_composite_nocolor_with_option(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "Scedilla"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;96m'Scedilla' path\x1b[0m" not in captured.out
    assert "'Scedilla' path" in captured.out
    assert "path.quadTo(728, -66, 699, -61)" in captured.out


def test_path_run_single_glyph_composite_nocolor_when_not_tty(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "Scedilla"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;96m'Scedilla' path\x1b[0m" not in captured.out
    assert "'Scedilla' path" in captured.out
    assert "path.quadTo(728, -66, 699, -61)" in captured.out


def test_path_run_single_glyph_no_contours_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, ".notdef"])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;96m'.notdef' path\x1b[0m" in captured.out
    assert "No contours" in captured.out


def test_path_run_full_glyph_set_default(capsys, monkeypatch):
    expected_glyphnames = [
        ".notdef",
        "A",
        "B",
        "C",
        "glyph00004",
        "a",
        "b",
        "c",
        "zero",
        "one",
        "two",
        "three",
        "comma",
        "Amacron",
        "Scedilla",
        "glyph00015",
        "glyph00016",
    ]

    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    for glyphname in expected_glyphnames:
        assert f"\x1b[1;96m'{glyphname}' path\x1b[0m" in captured.out

    assert "path.moveTo(869, 377)" in captured.out


def test_path_run_full_glyph_set_nocolor_flag(capsys, monkeypatch):
    expected_glyphnames = [
        ".notdef",
        "A",
        "B",
        "C",
        "glyph00004",
        "a",
        "b",
        "c",
        "zero",
        "one",
        "two",
        "three",
        "comma",
        "Amacron",
        "Scedilla",
        "glyph00015",
        "glyph00016",
    ]

    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1])
    path_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    for glyphname in expected_glyphnames:
        assert f"\x1b[1;96m'{glyphname}' path\x1b[0m" not in captured.out
        assert f"'{glyphname}' path" in captured.out

    assert "path.moveTo(869, 377)" in captured.out
