import argparse

from fontTools.ttLib import TTFont  # type: ignore
from fontTools.ttLib.tables._g_l_y_f import Glyph  # type: ignore

from .bridge import skia_path_to_ttfont_glyph, ttfont_glyph_to_skia_path
from .stringbuilder import cyan_bright_text
from .validators import validate_fontpath, validate_glyph_in_font


def contours_run(args: argparse.Namespace) -> None:
    """
    Parses command line arguments to `contours` sub-
    command and dumps glyph level contour data for
    a command line specified glyph name or the full
    glyph set.
    """
    fontpath: str = args.fontpath
    glyphname: str = args.glyphname

    # --------------------
    # CLI arg validations
    # --------------------
    validate_fontpath(fontpath)

    tt = TTFont(fontpath)
    glyf_table = tt["glyf"]

    if glyphname:
        # confirm that `glyphname` request is in the font
        validate_glyph_in_font(glyphname, tt)

        glyph = glyf_table[glyphname]
        print(
            f"[ {cyan_bright_text(glyphname, nocolor=args.nocolor)} ]: "
            f"{number_of_contours(glyphname, glyph, tt)}"
        )
    else:
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            glyph = glyf_table[local_glyphname]

            print(
                f"[ {cyan_bright_text(local_glyphname, nocolor=args.nocolor)} ]: "
                f"{number_of_contours(local_glyphname, glyph, tt)}"
            )


def number_of_contours(glyphname: str, glyph: Glyph, tt: TTFont) -> int:
    """
    Returns the number of contours in a glyph outline.  Composite
    glyphs are decomposed before assessment.
    """
    if glyph.isComposite():
        # decompose composite glyphs
        glyph = skia_path_to_ttfont_glyph(ttfont_glyph_to_skia_path(glyphname, tt))
    return glyph.numberOfContours
