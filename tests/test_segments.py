import argparse
import os

import pytest
from fontTools.ttLib import TTFont
from pathins.segments import segments_run
import pathins.stringbuilder


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


def test_segments_run_error_invalid_path(capsys):
    test_path = os.path.join("bogus", "path.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        segments_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_segments_run_error_non_font_path(capsys):
    test_path = os.path.join("tests", "testfiles", "text", "test.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        segments_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a TTF format font" in captured.err


def test_contours_run_fail_invalid_glyphname(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "bogus"])
    with pytest.raises(SystemExit) as e:
        segments_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "Failed to open glyph" in captured.err


def test_segments_run_single_glyph_nocontours_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, ".notdef"])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\033[1;96m'.notdef' segments\033[0m" in captured.out
    assert "No contours" in captured.out


def test_segments_run_single_glyph_nocontours_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, ".notdef"])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "'.notdef' segments" in captured.out
    assert "No contours" in captured.out


def test_segments_run_single_glyph_noncomposite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "A"])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\033[1;96m'A' segments\033[0m" in captured.out

    assert (
        f"\033[32m(545,0)\033[0m (459,221): \033[1;96mLINE\033[0m 237.14 units\n"
        f"(459,221) (176,221): \033[1;96mLINE\033[0m 283.00 units"
    ) in captured.out

    assert (
        f"(287,517) (206,301): \033[1;96mLINE\033[0m 230.69 units\n"
        f"\033[31m(206,301)\033[0m \033[32m(432,301)\033[0m: \033[1;96mLINE\033[0m 226.00 units"
    ) in captured.out


def test_segments_run_single_glyph_noncomposite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "A"])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "'A' segments" in captured.out

    assert (
        f"(545,0) (459,221): LINE 237.14 units\n"
        f"(459,221) (176,221): LINE 283.00 units"
    ) in captured.out

    assert (
        f"(287,517) (206,301): LINE 230.69 units\n"
        f"(206,301) (432,301): LINE 226.00 units"
    ) in captured.out


def test_segments_run_single_glyph_composite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "uni2E2E"])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\033[1;96m'uni2E2E' segments\033[0m" in captured.out

    assert (
        "\033[32m(303,201)\033[0m (303,228): \033[1;96mLINE\033[0m 27.00 units\n"
        "(303,228) (303,266) (296,294): \033[1;96mQCURVE\033[0m 66.53 units"
    ) in captured.out

    assert (
        "(309,2) \033[31m(326,18)\033[0m \033[32m(326,54)\033[0m: \033[1;96mQCURVE\033[0m 56.25 units"
        in captured.out
    )


def test_segments_run_single_glyph_composite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "uni2E2E"])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "'uni2E2E' segments" in captured.out

    assert (
        "(303,201) (303,228): LINE 27.00 units\n"
        "(303,228) (303,266) (296,294): QCURVE 66.53 units"
    ) in captured.out

    assert "(309,2) (326,18) (326,54): QCURVE 56.25 units" in captured.out


def test_segments_run_all_glyphs_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\033[1;96m'.notdef' segments\033[0m" in captured.out
    assert "\033[1;96m'space' segments\033[0m" in captured.out
    assert "\033[1;96m'comma' segments\033[0m" in captured.out
    assert "\033[1;96m'question' segments\033[0m" in captured.out
    assert "\033[1;96m'A' segments\033[0m" in captured.out
    assert "\033[1;96m'uni2E2E' segments\033[0m" in captured.out

    assert "\033[1mTotal\033[0m: 671.74 units" in captured.out
    assert "\033[1mTotal\033[0m: 2245.15 units" in captured.out
    assert "\033[1mTotal\033[0m: 3471.07 units" in captured.out
    assert "\033[1mTotal\033[0m: 2246.05 units" in captured.out


def test_segments_run_all_glyphs_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1])
    segments_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\033[1;96m'.notdef' segments\033[0m" not in captured.out
    assert "\033[1;96m'space' segments\033[0m" not in captured.out
    assert "\033[1;96m'comma' segments\033[0m" not in captured.out
    assert "\033[1;96m'question' segments\033[0m" not in captured.out
    assert "\033[1;96m'A' segments\033[0m" not in captured.out
    assert "\033[1;96m'uni2E2E' segments\033[0m" not in captured.out

    assert "'.notdef' segments" in captured.out
    assert "'space' segments" in captured.out
    assert "'comma' segments" in captured.out
    assert "'question' segments" in captured.out
    assert "'A' segments" in captured.out
    assert "'uni2E2E' segments" in captured.out

    assert "Total: 671.74 units" in captured.out
    assert "Total: 2245.15 units" in captured.out
    assert "Total: 3471.07 units" in captured.out
    assert "Total: 2246.05 units" in captured.out
