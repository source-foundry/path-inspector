import argparse
import sys

import pathops  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore

from .bridge import skia_path_to_ttfont_glyph, ttfont_glyph_to_skia_path
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

FLAG_ON_CURVE = 0x01


def temp_test(coords1, coords2, endpoints1, endpoints2, flags1, flags2):
    coordset1 = set()
    coordset2 = set()
    # fill with pre simplified glyph coordinates
    for coord in coords1:
        coordset1.add(coord)
    # fill with post simplified glyph coordinates
    for coord in coords2:
        coordset2.add(coord)

    print(flags1)
    print(endpoints1)
    # endpoints is a list of the *index* (in coordinates) of endpoint
    # for *each contour*!
    i = endpoints1[0]
    print(f"endpoint: {coords1[i]}")

    # print on/off curve status (0 = off curve, 1 = on curve)
    for x, coord in enumerate(coords1):
        print(coord, flags1[x] & FLAG_ON_CURVE)

    sys.exit()

    # empty segment check
    # TODO: add check that simplified path has fewer
    # coordinates and does not contain the empty segments
    for x, first_test_coord in enumerate(coords1):
        if x + 2 <= len(coords1):
            second_test_coord = coords1[x + 1]
            if first_test_coord == second_test_coord:
                print("Empty segment:")
                print(first_test_coord, second_test_coord)

    # collinear vector check
    # TODO: add check that simplified path does not contain
    # the collinear coordinates
    for x, begin_test_coord in enumerate(coords1):
        if x + 4 <= len(coords1):
            second_test_coord = coords1[x + 1]
            third_test_coord = coords1[x + 2]
            end_test_coord = coords1[x + 3]
            if (
                begin_test_coord[0]
                == second_test_coord[0]
                == third_test_coord[0]
                == end_test_coord[0]
            ):
                print("x-axis:")
                print(
                    begin_test_coord,
                    second_test_coord,
                    third_test_coord,
                    end_test_coord,
                )
            if (
                begin_test_coord[1]
                == second_test_coord[1]
                == third_test_coord[1]
                == end_test_coord[1]
            ):
                print("y-axis:")
                print(
                    begin_test_coord,
                    second_test_coord,
                    third_test_coord,
                    end_test_coord,
                )
    print(len(coordset1) > len(coordset2))
    print(coordset1.difference(coordset2))


def has_overlap(skia_path_pre: pathops.Path, glyf_table) -> bool:
    # if there are no contours, then there are no overlaps
    # skip pathops.simplify and diff check
    if len(list(skia_path_pre.contours)) == 0:
        return False
    # analyze skia simplified outline diff
    skia_path_post = pathops.simplify(skia_path_pre, clockwise=skia_path_pre.clockwise)

    if skia_path_pre != skia_path_post:
        # simplified skia paths do not match
        # let's confirm that this is not simply a
        # change in starting points
        ttglyph_pre = skia_path_to_ttfont_glyph(skia_path_pre)
        coords1, endpoints1, flags1 = ttglyph_pre.getCoordinates(glyf_table)
        ttglyph_post = skia_path_to_ttfont_glyph(skia_path_post)
        coords2, endpoints2, flags2 = ttglyph_post.getCoordinates(glyf_table)
        coordset1 = set()
        coordset2 = set()
        # fill with pre simplified glyph coordinates
        for coord in coords1:
            coordset1.add(coord)
        # fill with post simplified glyph coordinates
        for coord in coords2:
            coordset2.add(coord)

        #
        #
        #   TESTING
        #
        #
        temp_test(coords1, coords2, endpoints1, endpoints2, flags1, flags2)

        #
        #
        #   END TESTING
        #
        #

        if (len(coords1) == len(coords2)) and len(
            coordset1.symmetric_difference(coordset2)
        ) == 0:
            return False
        else:
            return True
    else:
        return False


def overlap_run(args: argparse.Namespace) -> None:
    fontpath: str = args.fontpath
    glyphname: str = args.glyphname

    # --------------------
    # CLI arg validations
    # --------------------
    validate_fontpath(fontpath)

    tt = TTFont(fontpath)

    # --check option implementation
    if args.check:
        # start with probable overlap list and fail early
        for probable_glyphname in PROBABLE_OVERLAPS:
            try:
                # confirm that the glyph is in the font
                tt["glyf"][probable_glyphname]  # type: ignore
                skia_path_pre = ttfont_glyph_to_skia_path(glyphname, tt)
                if has_overlap(skia_path_pre, tt["glyf"]):
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
                if has_overlap(skia_path_pre, tt["glyf"]):
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
            overlap_result(
                glyphname, has_overlap(skia_path_pre, tt["glyf"]), nocolor=args.nocolor
            )
        )
    else:
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            skia_path_pre = ttfont_glyph_to_skia_path(local_glyphname, tt)  # type: ignore
            print(
                overlap_result(
                    str(local_glyphname),
                    has_overlap(skia_path_pre, tt["glyf"]),
                    nocolor=args.nocolor,
                )
            )
