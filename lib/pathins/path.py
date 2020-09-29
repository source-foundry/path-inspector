import argparse

import pathops  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore

from .bridge import ttfont_glyph_to_skia_path
from .stringbuilder import path_header
from .validators import validate_fontpath, validate_glyph_in_font


def path_run(args: argparse.Namespace) -> None:
    fontpath: str = args.fontpath
    glyphname: str = args.glyphname

    # --------------------
    # CLI arg validations
    # --------------------
    validate_fontpath(fontpath)

    tt = TTFont(fontpath)

    skia_path: pathops.Path

    if glyphname:
        # confirm that `glyphname` request is in the font
        validate_glyph_in_font(glyphname, tt)

        skia_path = ttfont_glyph_to_skia_path(glyphname, tt)
        print(path_header(f"'{glyphname}' path", nocolor=args.nocolor))
        skia_path.dump()
    else:
        glyph_names = tt.getGlyphOrder()
        len_glyph_names = len(glyph_names)
        for x, local_glyphname in enumerate(glyph_names):
            skia_path = ttfont_glyph_to_skia_path(local_glyphname, tt)
            print(path_header(f"'{local_glyphname}' path", nocolor=args.nocolor))
            skia_path.dump()
            if x + 1 < len_glyph_names:
                # append a newline to all glyph reports except last
                print("")
