import argparse

import pathops  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore

from .bridge import ttfont_glyph_to_skia_path
from .stringbuilder import direction_result
from .validators import validate_fontpath, validate_glyph_in_font

# TODO: add --check support to confirm all paths in same direction
# TODO: add --summary to include total CW and CCW directions


def direction_run(args: argparse.Namespace) -> None:
    """
    Displays the direction of the outermost contour of one
    or more glyphs in a font.  Results are expressed as either
    "clockwise" or "counter-clockwise".
    """
    fontpath: str = args.fontpath
    glyphname: str = args.glyphname

    # --------------------
    # CLI arg validations
    # --------------------
    validate_fontpath(fontpath)

    tt = TTFont(fontpath)

    skia_path: pathops.Path

    if glyphname:
        validate_glyph_in_font(glyphname, tt)
        skia_path = ttfont_glyph_to_skia_path(glyphname, tt)
        print(
            direction_result(
                glyphname,
                skia_path.clockwise,
                len(list(skia_path.contours)),
                nocolor=args.nocolor,
            )
        )
    else:
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            skia_path = ttfont_glyph_to_skia_path(local_glyphname, tt)  # type: ignore
            print(
                direction_result(
                    str(local_glyphname),
                    skia_path.clockwise,
                    len(list(skia_path.contours)),
                    nocolor=args.nocolor,
                )
            )
