import argparse
import os
import sys

from fontTools.ttLib import TTFont
import pytest

from pathins.contours import contours_run, number_of_contours

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


def test_number_of_contours_noncomposite():
    glyphname = "A"
    tt = TTFont(TESTFONT_PATH_1)
    glyf_table = tt["glyf"]
    glyph = glyf_table[glyphname]

    contour_number = number_of_contours(glyphname, glyph, tt)
    assert contour_number == 2


def test_number_of_contours_composite():
    glyphname = "uni2E2E"
    tt = TTFont(TESTFONT_PATH_1)
    glyf_table = tt["glyf"]
    glyph = glyf_table[glyphname]

    contour_number = number_of_contours(glyphname, glyph, tt)
    assert contour_number == 2


def test_contours_run_error_invalid_path(capsys):
    test_path = os.path.join("bogus", "path.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        contours_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_contours_run_error_non_font_path(capsys):
    test_path = os.path.join("tests", "testfiles", "text", "test.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        contours_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a TTF format font" in captured.err


def test_contours_run_fail_invalid_glyphname(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "bogus"])
    with pytest.raises(SystemExit) as e:
        contours_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "Failed to open glyph" in captured.err


def test_contours_run_single_glyph_noncomposite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "A"])
    contours_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ \x1b[1;96mA\x1b[0m ]: 2" in captured.out


def test_contours_run_single_glyph_noncomposite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "A"])
    contours_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ A ]: 2" in captured.out


def test_contours_run_single_glyph_composite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "uni2E2E"])
    contours_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ \x1b[1;96muni2E2E\x1b[0m ]: 2" in captured.out


def test_contours_run_single_glyph_composite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "uni2E2E"])
    contours_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ uni2E2E ]: 2" in captured.out


def test_contours_run_multi_glyph_composite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1])
    contours_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ \x1b[1;96m.notdef\x1b[0m ]: 0" in captured.out
    assert "[ \x1b[1;96mspace\x1b[0m ]: 0" in captured.out
    assert "[ \x1b[1;96mcomma\x1b[0m ]: 1" in captured.out
    assert "[ \x1b[1;96mquestion\x1b[0m ]: 2" in captured.out
    assert "[ \x1b[1;96mA\x1b[0m ]: 2" in captured.out
    assert "[ \x1b[1;96muni2E2E\x1b[0m ]: 2" in captured.out


def test_contours_run_multi_glyph_composite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1])
    contours_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "[ .notdef ]: 0" in captured.out
    assert "[ space ]: 0" in captured.out
    assert "[ comma ]: 1" in captured.out
    assert "[ question ]: 2" in captured.out
    assert "[ A ]: 2" in captured.out
    assert "[ uni2E2E ]: 2" in captured.out
