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

# TODO: add number of contours check before the simplify step, if none then can skip
# because there will be no overlap


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
                if len(list(skia_path_pre.contours)) == 0:
                    # if there are no contours, there are no overlaps
                    # skip pathops.simplify and diff check
                    pass
                else:
                    skia_path_post = pathops.simplify(
                        skia_path_pre, clockwise=skia_path_pre.clockwise
                    )
                    if skia_path_pre != skia_path_post:
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
                if len(list(skia_path_pre.contours)) == 0:
                    # if there are no contours, there is no overlap
                    # skip pathops.simplify and diff check
                    pass
                else:
                    skia_path_post = pathops.simplify(
                        skia_path_pre, clockwise=skia_path_pre.clockwise
                    )
                    if skia_path_pre != skia_path_post:
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
        if len(list(skia_path_pre.contours)) == 0:
            # if there are no contours, there is no overlap
            # skip pathops.simplify and diff check
            # declare test_pass parameter = False
            print(overlap_result(glyphname, False, nocolor=args.nocolor))
        else:
            skia_path_post = pathops.simplify(
                skia_path_pre, clockwise=skia_path_pre.clockwise
            )
            # pass = has overlap
            # fail = no overlap
            test_pass: bool = skia_path_pre != skia_path_post
            print(overlap_result(glyphname, test_pass, nocolor=args.nocolor))
    else:
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            skia_path_pre = ttfont_glyph_to_skia_path(local_glyphname, tt)  # type: ignore
            if len(list(skia_path_pre.contours)) == 0:
                # if there are no contours, there is no overlap
                # skip pathops.simplify and diff check
                # declare test_pass parameter = False
                print(
                    overlap_result(
                        local_glyphname, False, nocolor=args.nocolor  # type: ignore
                    )
                )
            else:
                skia_path_post = pathops.simplify(
                    skia_path_pre, clockwise=skia_path_pre.clockwise
                )
                # pass = has overlap
                # fail = no overlap
                test_pass = skia_path_pre != skia_path_post
                print(
                    overlap_result(
                        str(local_glyphname), test_pass, nocolor=args.nocolor
                    )
                )
