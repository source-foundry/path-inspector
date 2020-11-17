import argparse
from typing import Sequence, Tuple

import pathops  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore
from fontTools.ttLib.tables._g_l_y_f import Glyph  # type: ignore

from .bridge import ttfont_glyph_to_skia_path
from .stringbuilder import direction_result
from .validators import validate_fontpath, validate_glyph_in_font

# TODO: add --summary to include total CW and CCW directions


def direction_run(args: argparse.Namespace) -> None:
    """
    Displays the direction of the outermost contour(s) of one
    or more glyphs in a font.  Results are expressed as either
    "clockwise" or "counter-clockwise".  The report includes
    the x, y scaling factors for transfomed components of
    composite glyphs.  This scaling *may* reverse the path
    direction that is reported for the decomposed outline.
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

        # transformed components can change path direction
        # in the decomposed paths
        # (e.g. 180 degree Y-axis rotation = mirroring)
        # add base component glyph name and transform values
        # to the report if this is present
        glyph = tt["glyf"][glyphname]
        components_with_transforms: Sequence[Tuple] = []
        if glyph.isComposite():
            components_with_transforms = _get_components_with_transforms(glyph)

        print(
            direction_result(
                glyphname,
                skia_path.clockwise,
                len(list(skia_path.contours)),
                components_with_transforms=components_with_transforms,
                nocolor=args.nocolor,
            )
        )
    else:
        glyph_names = tt.getGlyphOrder()
        for local_glyphname in glyph_names:
            glyph = tt["glyf"][local_glyphname]
            components_with_transforms = []

            # transformed components can change path direction
            # in the decomposed paths
            # (e.g. 180 degree Y-axis rotation = mirroring)
            # add base component glyph name and transform values
            # to the report if this is present
            if glyph.isComposite():
                components_with_transforms = _get_components_with_transforms(glyph)

            skia_path = ttfont_glyph_to_skia_path(local_glyphname, tt)  # type: ignore

            print(
                direction_result(
                    str(local_glyphname),
                    skia_path.clockwise,
                    len(list(skia_path.contours)),
                    components_with_transforms=components_with_transforms,
                    nocolor=args.nocolor,
                )
            )


def _get_components_with_transforms(glyph: Glyph) -> Sequence[Tuple]:
    """
    Returns list with component glyph names and x,y transforms
    for composite glyphs with transforms. In all other cases,
    returns an empty list
    """
    components_with_transforms = []
    if glyph.isComposite():
        for component in glyph.components:
            if hasattr(component, "transform"):
                # transform attribute will include one of the
                # following data sets:
                # (1) simple X and Y scale only @ [0][0]
                # (2) x-scale @ [0][0] and y-scale @ [1][1]
                # (3) x-scale @ [0][0], scale01 @ [0][1],
                #     y-scale @ [1][1], scale10 @ [1][0]
                a1 = round(component.transform[0][0], 3)
                a2 = round(component.transform[0][1], 3)
                b1 = round(component.transform[1][0], 3)
                b2 = round(component.transform[1][1], 3)
                components_with_transforms.append(
                    (component.glyphName, [[a1, a2], [b1, b2]])
                )
    return components_with_transforms
