import pathops  # type: ignore
from fontTools.pens.recordingPen import DecomposingRecordingPen  # type: ignore
from fontTools.pens.ttGlyphPen import TTGlyphPen  # type: ignore
from fontTools.ttLib import ttFont  # type: ignore
from fontTools.ttLib.tables import _g_l_y_f  # type: ignore


def ttfont_glyph_to_skia_path(glyph_name: str, tt_font: ttFont.TTFont) -> pathops.Path:
    glyf_table = tt_font["glyf"]
    glyph_set: ttFont._TTGlyphSet = tt_font.getGlyphSet()
    tt_glyph = glyf_table[glyph_name]
    skia_path = pathops.Path()
    skia_path_pen = skia_path.getPen()

    if tt_glyph.isComposite():
        decompose_pen = DecomposingRecordingPen(glyph_set)
        glyph_set[glyph_name].draw(decompose_pen)
        decompose_pen.replay(skia_path_pen)
        return skia_path
    else:
        glyph_set[glyph_name].draw(skia_path_pen)
        return skia_path


def skia_path_to_ttfont_glyph(skia_path: pathops.Path) -> _g_l_y_f.Glyph:
    tt_pen = TTGlyphPen(glyphSet=None)
    skia_path.draw(tt_pen)
    glyph = tt_pen.glyph()
    assert not glyph.isComposite()
    glyph.recalcBounds(glyfTable=None)
    return glyph
