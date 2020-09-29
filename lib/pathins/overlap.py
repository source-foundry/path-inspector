import argparse
import sys

import pathops  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore

from .bridge import ttfont_glyph_to_skia_path
from .stringbuilder import overlap_result
from .validators import validate_fontpath, validate_glyph_in_font

PROBABLE_OVERLAPS = [
    "Q",
    "numbersign",
    "plus",
    "A",
    "notequal",
    "ampersand",
    "K",
    "Eth",
    "Dcroat",
    "Hbar",
    "uni0424",
    "uni04FE",
    "uni048E",
    "uni03A6",
    "uni03A8",
]


def has_overlap(skia_path_pre: pathops.Path) -> bool:
    # if there are no contours, then there are no overlaps
    # skip pathops.simplify and diff check
    if len(list(skia_path_pre.contours)) == 0:
        return False
    # analyze skia simplified outline diff
    skia_path_post = pathops.simplify(skia_path_pre, clockwise=skia_path_pre.clockwise)
    return skia_path_pre != skia_path_post


def overlap_run(args: argparse.Namespace) -> None:
    fontpath: str = args.fontpath
    glyphname: str = args.glyphname

    # --------------------
    # CLI arg validations
    # --------------------
    validate_fontpath(fontpath)

    tt = TTFont(fontpath)

    skia_path_pre: pathops.Path
    skia_path_post: pathops.Path

    # --check option implementation
    if args.check:
        # start with probable overlap list and fail early
        for probable_glyphname in PROBABLE_OVERLAPS:
            try:
                # confirm that the glyph is in the font
                tt["glyf"][probable_glyphname]  # type: ignore
                skia_path_pre = ttfont_glyph_to_skia_path(glyphname, tt)
                if has_overlap(skia_path_pre):
                    print(f"{fontpath}: overlapping paths are present")
                    sys.exit(1)
            # if the glyph is not present in the font
            # raises KeyError and we skip it
            except KeyError:
                pass
        # if no overlaps found on the probable list
        # continue with the full glyph set
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            # do not need to repeat check on glyphs that
            # were already analyzed
            if local_glyphname not in PROBABLE_OVERLAPS:
                skia_path_pre = ttfont_glyph_to_skia_path(
                    local_glyphname, tt  # type: ignore
                )
                if has_overlap(skia_path_pre):
                    print(f"{fontpath}: overlapping paths are present")
                    sys.exit(1)

        # if we made it this far, then there were no overlapping paths
        print(f"{fontpath}: no overlapping paths")
        sys.exit(0)

    # default implementation
    if glyphname:
        # confirm that `glyphname` request is in the font
        validate_glyph_in_font(glyphname, tt)
        skia_path_pre = ttfont_glyph_to_skia_path(glyphname, tt)
        print(
            overlap_result(glyphname, has_overlap(skia_path_pre), nocolor=args.nocolor)
        )
    else:
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            skia_path_pre = ttfont_glyph_to_skia_path(local_glyphname, tt)  # type: ignore
            print(
                overlap_result(
                    str(local_glyphname),
                    has_overlap(skia_path_pre),
                    nocolor=args.nocolor,
                )
            )
