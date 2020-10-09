import argparse
import os
from typing import List

from fontTools.misc.bezierTools import calcQuadraticArcLength  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore
from fontTools.ttLib.tables._g_l_y_f import Glyph  # type: ignore

from .bezier import quadratic_path
from .bridge import skia_path_to_ttfont_glyph, ttfont_glyph_to_skia_path
from .datastructures import Coordinate
from .math import linear_distance_between_coordinates
from .stringbuilder import (
    report_header,
    segment_line,
    segment_quadratic_curve,
    segment_total_distance,
)
from .validators import validate_fontpath, validate_glyph_in_font


def segments_run(args: argparse.Namespace) -> None:
    """
    Parses command line arguments to the `segments`
    sub-command and dumps segment data for a
    command line specified glyph name or the full
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

        glyph: Glyph = glyf_table[glyphname]

        # decompose composite glyphs
        if glyph.isComposite():
            glyph = skia_path_to_ttfont_glyph(ttfont_glyph_to_skia_path(glyphname, tt))

        # define new quadratic path coordinates with *implied*
        # on curve points to support the arc distance calculations
        coords: List[Coordinate] = quadratic_path(glyph, glyf_table, include_implied=True)

        print(report_header(f"'{glyphname}' segments", nocolor=args.nocolor))
        if len(coords) == 0:
            print("   No contours")
        else:
            _print_segments(coords, args.nocolor)
    # full glyph set
    else:
        glyph_names = tt.getGlyphOrder()
        len_glyph_names = len(glyph_names)
        for x, local_glyphname in enumerate(glyph_names):
            glyph = glyf_table[local_glyphname]

            # decompose composite glyphs
            if glyph.isComposite():
                glyph = skia_path_to_ttfont_glyph(
                    ttfont_glyph_to_skia_path(local_glyphname, tt)
                )
            coords = quadratic_path(glyph, glyf_table, include_implied=True)

            print(report_header(f"'{local_glyphname}' segments", nocolor=args.nocolor))
            if len(coords) == 0:
                print("   No contours")
            else:
                _print_segments(coords, args.nocolor)
            if x + 1 < len_glyph_names:
                # append a newline to all glyph reports except last
                print("")


def _print_segments(coords: List[Coordinate], nocolor: bool) -> None:
    start_coord = None
    total_distance: float = 0.0
    for coord in coords:
        # keep start coordinate for calculation of final
        # contour point distances as curve is closed
        if coord.startpoint:
            start_coord = coord
            # nothing to do at the start coordinate
            continue

        if coord.oncurve:
            # we are on the curve, check previous point to see if this
            # is a line or quadratic curve segment
            if coord.coord_previous:
                if coord.coord_previous.oncurve:
                    distance = linear_distance_between_coordinates(
                        (coord.coord_previous.x, coord.coord_previous.y),
                        (coord.x, coord.y),
                    )
                    line_string = segment_line(
                        coord.coord_previous,
                        coord,
                        distance,
                        nocolor,
                    )
                    total_distance += distance
                    print(line_string)
                else:
                    pass

            if coord.endpoint and start_coord:
                # add the endpoint to startpoint segment if the endpoint is oncurve
                # note: this is a forward direction write in contrast to previous
                #       logic which checks backwards
                distance = linear_distance_between_coordinates(
                    (coord.x, coord.y), (start_coord.x, start_coord.y)
                )
                line_string = segment_line(coord, start_coord, distance, nocolor)
                total_distance += distance
                print(line_string)
        # we have an off-curve point
        else:
            if coord.endpoint and coord.coord_previous and start_coord:
                distance = calcQuadraticArcLength(
                    (coord.coord_previous.x, coord.coord_previous.y),
                    (coord.x, coord.y),
                    (start_coord.x, start_coord.y),
                )
                qcurve_string = segment_quadratic_curve(
                    coord.coord_previous, coord, start_coord, distance, nocolor
                )
                total_distance += distance
                print(qcurve_string)
            elif coord.coord_previous and coord.coord_next:
                assert coord.coord_previous.oncurve is True
                assert coord.coord_next.oncurve is True
                distance = calcQuadraticArcLength(
                    (coord.coord_previous.x, coord.coord_previous.y),
                    (coord.x, coord.y),
                    (coord.coord_next.x, coord.coord_next.y),
                )
                qcurve_string = segment_quadratic_curve(
                    coord.coord_previous,
                    coord,
                    coord.coord_next,
                    distance,
                    nocolor,
                )
                total_distance += distance
                print(qcurve_string)

    print(f"{os.linesep} {segment_total_distance(total_distance, nocolor=nocolor)}")
