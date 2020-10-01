import os

import pytest

from fontTools.ttLib import TTFont

from pathins.bridge import skia_path_to_ttfont_glyph, ttfont_glyph_to_skia_path

TESTFONT_PATH_1 = os.path.join("tests", "testfiles", "fonts", "RobotoMono-subset1.ttf")


def test_ttfont_glyph_to_skia_path_non_composite():
    tt = TTFont(TESTFONT_PATH_1)
    skia_path = ttfont_glyph_to_skia_path("A", tt)
    assert len(list(skia_path.contours)) == 2
    assert "path.moveTo(869, 377)" in str(skia_path)


def test_ttfont_glyph_to_skia_path_composite():
    tt = TTFont(TESTFONT_PATH_1)
    skia_path = ttfont_glyph_to_skia_path("Scedilla", tt)
    # has overlapping S form and cedilla contours
    assert len(list(skia_path.contours)) == 2
    assert "path.moveTo(936, 368)" in str(skia_path)


def test_skia_path_to_ttfont_glyph_non_composite():
    tt = TTFont(TESTFONT_PATH_1)
    skia_path = ttfont_glyph_to_skia_path("A", tt)
    glyph = skia_path_to_ttfont_glyph(skia_path)
    assert glyph.numberOfContours == 2
    assert glyph.isComposite() is False


def test_skia_path_to_ttfont_glyph_composite():
    tt = TTFont(TESTFONT_PATH_1)
    skia_path = ttfont_glyph_to_skia_path("Scedilla", tt)
    glyph = skia_path_to_ttfont_glyph(skia_path)
    assert glyph.numberOfContours == 2
    # the original composite outlines are decomposed
    # during when converted to skia path
    assert glyph.isComposite() is False
