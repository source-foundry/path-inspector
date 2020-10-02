import argparse
import os
import sys

import pytest

from pathins.coordinates import coordinates_run

TESTFONT_PATH_1 = os.path.join(
    "tests", "testfiles", "fonts", "NotoSans-Regular.subset1.ttf"
)

COLORED_START = "\033[32mSTART ~~~~~~~~\033[0m"
COLORED_END = "\033[31m~~~~~~~~~~ END\033[0m"
UNCOLORED_START = "START ~~~~~~~~"
UNCOLORED_END = "~~~~~~~~~~ END"
ON_PATH = "----- on -----"

# instantiate a parser for unit tests in this module
parser = argparse.ArgumentParser()
parser.add_argument("--nocolor", action="store_true", help="no ANSI color")
parser.add_argument("fontpath", type=str, help="font file path")
parser.add_argument(
    "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
)


def test_coordinates_run_error_invalid_path(capsys):
    test_path = os.path.join("bogus", "path.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        coordinates_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_coordinates_run_error_non_font_path(capsys):
    test_path = os.path.join("tests", "testfiles", "text", "test.txt")
    args = parser.parse_args([test_path])

    with pytest.raises(SystemExit) as e:
        coordinates_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "does not appear to be a TTF format font" in captured.err


def test_coordinates_run_fail_invalid_glyphname(capsys):
    args = parser.parse_args([TESTFONT_PATH_1, "bogus"])
    with pytest.raises(SystemExit) as e:
        coordinates_run(args)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert "Failed to open glyph" in captured.err


def test_coordinates_run_single_glyph_noncomposite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "A"])
    coordinates_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;36m'A' coordinates\x1b[0m" in captured.out
    # check first contour start coordinate appropriately labeled
    assert f"(545, 0) {COLORED_START}" in captured.out
    assert f"(459, 221) {ON_PATH}" in captured.out
    # check first contour end coord appropriately labeled
    assert f"(638, 0) {COLORED_END}" in captured.out
    # check second contour start coordinate appropriately labeled
    assert f"(432, 301) {COLORED_START}" in captured.out
    assert "(349, 525)" in captured.out
    # check off-curve coordinate appropriately labeled
    assert f"(349, 525) {ON_PATH}" not in captured.out
    # check second contour end coordinate appropriately labeled
    assert f"(206, 301) {COLORED_END}" in captured.out


def test_coordinates_run_single_glyph_noncomposite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "A"])
    coordinates_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;36m'A' coordinates\x1b[0m" not in captured.out
    assert "'A' coordinates" in captured.out
    # check first contour start coordinate appropriately labeled
    assert f"(545, 0) {COLORED_START}" not in captured.out
    assert f"(545, 0) {UNCOLORED_START}" in captured.out

    assert f"(459, 221) {ON_PATH}" in captured.out

    # check first contour end coord appropriately labeled
    assert f"(638, 0) {COLORED_END}" not in captured.out
    assert f"(638, 0) {UNCOLORED_END}" in captured.out

    # check second contour start coordinate appropriately labeled
    assert f"(432, 301) {COLORED_START}" not in captured.out
    assert f"(432, 301) {UNCOLORED_START}" in captured.out

    # check off-curve coordinate appropriately labeled
    assert "(349, 525)" in captured.out
    assert f"(349, 525) {ON_PATH}" not in captured.out

    # check second contour end coordinate appropriately labeled
    assert f"(206, 301) {COLORED_END}" not in captured.out
    assert f"(206, 301) {UNCOLORED_END}" in captured.out


def test_coordinates_run_single_glyph_composite_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1, "uni2E2E"])
    coordinates_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;36m'uni2E2E' coordinates\x1b[0m" in captured.out

    assert f"(303, 201) {COLORED_START}" in captured.out
    assert f"(303, 228) {ON_PATH}" in captured.out

    assert "(303, 266)" in captured.out
    assert f"(303, 266) {ON_PATH}" not in captured.out

    assert f"(233, 201) {COLORED_END}" in captured.out

    assert f"(326, 54) {COLORED_START}" in captured.out

    assert "(326, 91)" in captured.out
    assert f"(326, 91) {ON_PATH}" not in captured.out

    assert f"(264, -14) {ON_PATH}" in captured.out

    assert f"(326, 18) {COLORED_END}" in captured.out


def test_coordinates_run_single_glyph_composite_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1, "uni2E2E"])
    coordinates_run(args)

    captured = capsys.readouterr()
    # must be in a tty to get ANSI color output
    # this is mocked above
    assert "\x1b[1;36m'uni2E2E' coordinates\x1b[0m" not in captured.out
    assert "'uni2E2E' coordinates" in captured.out

    assert f"(303, 201) {UNCOLORED_START}" in captured.out
    assert f"(303, 228) {ON_PATH}" in captured.out

    assert "(303, 266)" in captured.out
    assert f"(303, 266) {ON_PATH}" not in captured.out

    assert f"(233, 201) {UNCOLORED_END}" in captured.out

    assert f"(326, 54) {UNCOLORED_START}" in captured.out

    assert "(326, 91)" in captured.out
    assert f"(326, 91) {ON_PATH}" not in captured.out

    assert f"(264, -14) {ON_PATH}" in captured.out

    assert f"(326, 18) {UNCOLORED_END}" in captured.out


def test_coordinates_run_multi_glyph_default(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args([TESTFONT_PATH_1])
    coordinates_run(args)

    captured = capsys.readouterr()

    # confirm all expected glyphs are included
    assert "\x1b[1;36m'.notdef' coordinates\x1b[0m" in captured.out
    assert "\x1b[1;36m'space' coordinates\x1b[0m" in captured.out
    assert "\x1b[1;36m'comma' coordinates\x1b[0m" in captured.out
    assert "\x1b[1;36m'question' coordinates\x1b[0m" in captured.out
    assert "\x1b[1;36m'A' coordinates\x1b[0m" in captured.out
    assert "\x1b[1;36m'uni2E2E' coordinates\x1b[0m" in captured.out

    # check start paths across the glyphs
    assert f"(185, 116) {COLORED_START}" in captured.out
    assert f"(140, 201) {COLORED_START}" in captured.out
    assert f"(117, 54) {COLORED_START}" in captured.out
    assert f"(545, 0) {COLORED_START}" in captured.out
    assert f"(432, 301) {COLORED_START}" in captured.out
    assert f"(303, 201) {COLORED_START}" in captured.out
    assert f"(326, 54) {COLORED_START}" in captured.out

    # check end paths across the glyphs
    assert f"(91, 116) {COLORED_END}" in captured.out
    assert f"(210, 201) {COLORED_END}" in captured.out
    assert f"(117, 18) {COLORED_END}" in captured.out
    assert f"(638, 0) {COLORED_END}" in captured.out
    assert f"(206, 301) {COLORED_END}" in captured.out
    assert f"(233, 201) {COLORED_END}" in captured.out
    assert f"(326, 18) {COLORED_END}" in captured.out

    # check glyphs with no contours across the glyphs
    x = 1
    lines = captured.out.split("\n")
    for line in lines:
        if x == 4 or x == 9:
            assert "No contours" in line
        x += 1

    # spot check on-path coordinates in noncomposite glyphs
    assert f"(140, 228) {ON_PATH}" in captured.out
    assert f"(352, 517) {ON_PATH}" in captured.out
    assert f"(240, 54) {ON_PATH}" in captured.out

    # spot check off-path coordinates in noncomposite glyphs
    assert f"(130, -75) {ON_PATH}" not in captured.out
    assert "(130, -75)" in captured.out

    assert f"(210, 246) {ON_PATH}" not in captured.out
    assert "(210, 246)" in captured.out

    assert f"(322, 612) {ON_PATH}" not in captured.out
    assert "(322, 612)" in captured.out

    assert f"(251, 370) {ON_PATH}" not in captured.out
    assert "(251, 370)" in captured.out

    assert f"(203, 91) {ON_PATH}" not in captured.out
    assert "(203, 91)" in captured.out


def test_coordinates_run_multi_glyph_nocolor(capsys, monkeypatch):
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(sys.stdout, "isatty", mock_isatty)

    args = parser.parse_args(["--nocolor", TESTFONT_PATH_1])
    coordinates_run(args)

    captured = capsys.readouterr()

    # confirm all expected glyphs are included
    assert "\x1b[1;36m'.notdef' coordinates\x1b[0m" not in captured.out
    assert "\x1b[1;36m'space' coordinates\x1b[0m" not in captured.out
    assert "\x1b[1;36m'comma' coordinates\x1b[0m" not in captured.out
    assert "\x1b[1;36m'question' coordinates\x1b[0m" not in captured.out
    assert "\x1b[1;36m'A' coordinates\x1b[0m" not in captured.out
    assert "\x1b[1;36m'uni2E2E' coordinates\x1b[0m" not in captured.out

    assert "'.notdef' coordinates" in captured.out
    assert "'space' coordinates" in captured.out
    assert "'comma' coordinates" in captured.out
    assert "'question' coordinates" in captured.out
    assert "'A' coordinates" in captured.out
    assert "'uni2E2E' coordinates" in captured.out

    # check start paths across the glyphs
    assert f"(185, 116) {COLORED_START}" not in captured.out
    assert f"(140, 201) {COLORED_START}" not in captured.out
    assert f"(117, 54) {COLORED_START}" not in captured.out
    assert f"(545, 0) {COLORED_START}" not in captured.out
    assert f"(432, 301) {COLORED_START}" not in captured.out
    assert f"(303, 201) {COLORED_START}" not in captured.out
    assert f"(326, 54) {COLORED_START}" not in captured.out

    assert f"(185, 116) {UNCOLORED_START}" in captured.out
    assert f"(140, 201) {UNCOLORED_START}" in captured.out
    assert f"(117, 54) {UNCOLORED_START}" in captured.out
    assert f"(545, 0) {UNCOLORED_START}" in captured.out
    assert f"(432, 301) {UNCOLORED_START}" in captured.out
    assert f"(303, 201) {UNCOLORED_START}" in captured.out
    assert f"(326, 54) {UNCOLORED_START}" in captured.out

    # check end paths across the glyphs
    assert f"(91, 116) {COLORED_END}" not in captured.out
    assert f"(210, 201) {COLORED_END}" not in captured.out
    assert f"(117, 18) {COLORED_END}" not in captured.out
    assert f"(638, 0) {COLORED_END}" not in captured.out
    assert f"(206, 301) {COLORED_END}" not in captured.out
    assert f"(233, 201) {COLORED_END}" not in captured.out
    assert f"(326, 18) {COLORED_END}" not in captured.out

    assert f"(91, 116) {UNCOLORED_END}" in captured.out
    assert f"(210, 201) {UNCOLORED_END}" in captured.out
    assert f"(117, 18) {UNCOLORED_END}" in captured.out
    assert f"(638, 0) {UNCOLORED_END}" in captured.out
    assert f"(206, 301) {UNCOLORED_END}" in captured.out
    assert f"(233, 201) {UNCOLORED_END}" in captured.out
    assert f"(326, 18) {UNCOLORED_END}" in captured.out

    # check glyphs with no contours across the glyphs
    x = 1
    lines = captured.out.split("\n")
    for line in lines:
        if x == 4 or x == 9:
            assert "No contours" in line
        x += 1

    # spot check on-path coordinates in noncomposite glyphs
    assert f"(140, 228) {ON_PATH}" in captured.out
    assert f"(352, 517) {ON_PATH}" in captured.out
    assert f"(240, 54) {ON_PATH}" in captured.out

    # spot check off-path coordinates in noncomposite glyphs
    assert f"(130, -75) {ON_PATH}" not in captured.out
    assert "(130, -75)" in captured.out

    assert f"(210, 246) {ON_PATH}" not in captured.out
    assert "(210, 246)" in captured.out

    assert f"(322, 612) {ON_PATH}" not in captured.out
    assert "(322, 612)" in captured.out

    assert f"(251, 370) {ON_PATH}" not in captured.out
    assert "(251, 370)" in captured.out

    assert f"(203, 91) {ON_PATH}" not in captured.out
    assert "(203, 91)" in captured.out
