import argparse

from fontTools.ttLib import TTFont  # type: ignore

from .bridge import ttfont_glyph_to_skia_path
from .stringbuilder import report_header
from .validators import validate_fontpath, validate_glyph_in_font


def report_run(args: argparse.Namespace) -> None:
    fontpath: str = args.fontpath
    glyphname: str = args.glyphname

    # --------------------
    # CLI arg validations
    # --------------------
    validate_fontpath(fontpath)

    tt = TTFont(fontpath)

    # confirm that `glyphname` request is in the font
    validate_glyph_in_font(glyphname, tt)

    skia_path = ttfont_glyph_to_skia_path(glyphname, tt)

    # Path dump from skia
    print(report_header(f"'{glyphname}' path"))
    skia_path.dump()
