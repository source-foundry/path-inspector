import argparse
import os
import sys
from typing import Any

from fontTools.ttLib import TTFont  # type: ignore
from fontTools.ttLib.tables._g_l_y_f import Glyph  # type: ignore

from .bridge import skia_path_to_ttfont_glyph, ttfont_glyph_to_skia_path
from .stringbuilder import green_text, red_text, report_header
from .validators import validate_fontpath, validate_glyph_in_font

FLAG_ON_CURVE = 0x01

ON_OFF = ["", "----- on -----"]
START_STRING = "START ~~~~~~~~"
END_STRING = "~~~~~~~~~~ END"


def coordinates_run(args: argparse.Namespace) -> None:
    """
    Parses command line arguments to the `coordinates`
    sub-command and dumps glyph contour coordinates,
    start points, end points, and on-/off-curve indicators
    for a command line specified glyph name or the full
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

        # decompose composite glyphs
        if glyph.isComposite():
            glyph = skia_path_to_ttfont_glyph(ttfont_glyph_to_skia_path(glyphname, tt))

        print(report_header(f"'{glyphname}' coordinates", nocolor=args.nocolor))
        sys.stdout.write(coordinates_report(glyph, glyf_table, nocolor=args.nocolor))
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

            print(report_header(f"'{local_glyphname}' coordinates", nocolor=args.nocolor))
            sys.stdout.write(coordinates_report(glyph, glyf_table, nocolor=args.nocolor))
            if x + 1 < len_glyph_names:
                # append a newline to all glyph reports except last
                print("")


def coordinates_report(glyph: Glyph, glyf_table: Any, nocolor: bool) -> str:
    """
    Returns a coordinates report string from glyph-level parameter
    data.
    """
    if glyph.numberOfContours > 0:
        coords, endpoints, flags = glyph.getCoordinates(glyf_table)

        endpoint_coordinates = [coords[endpoint] for endpoint in endpoints]

        coordinates_string: str = ""
        for x, coord in enumerate(coords):
            # on- and off-curve points are defined in
            # the `flags` integer array that are mapped
            # 1:1 to coordinate indices
            # test the on curve bit mask here and
            # use this to define the appropriate
            # string value in the report
            on_off = ON_OFF[flags[x] & FLAG_ON_CURVE]
            # this is a start coordinate if it
            # (1) is the first coordinate in the iterable
            # (2) follows a previous endpoint coordinate
            start_coord = (x == 0) or (coords[x - 1] in endpoint_coordinates)
            if start_coord:
                coordinates_string += (
                    f"{str(coord): >13} "
                    f"{green_text(START_STRING, nocolor=nocolor): <13}{os.linesep}"
                )
            # end coordinates are defined by the indices returned
            # in the Glyph.getGlyphCoordinates method return tuple
            # compare current test coordinate with those coordinate
            # values
            elif coords[x] in endpoint_coordinates:
                coordinates_string += (
                    f"{str(coord): >13} "
                    f"{red_text(END_STRING, nocolor=nocolor): <13}{os.linesep}"
                )
            else:
                coordinates_string += f"{str(coord): >13} {on_off: >13}{os.linesep}"

        return coordinates_string
    else:
        return f"   No contours{os.linesep}"
