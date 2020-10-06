from .math import midpoint_between_coordinates
from typing import Any, List

from fontTools.ttLib.tables._g_l_y_f import Glyph  # type: ignore

from .datastructures import Coordinate

FLAG_ON_CURVE = 0x01


def quadratic_path(
    glyph: Glyph, glyf_table: Any, include_implied=False
) -> List[Coordinate]:
    coords, endpoints, flags = glyph.getCoordinates(glyf_table)
    endpoint_coordinates = [coords[endpoint] for endpoint in endpoints]
    new_coords: List[Coordinate] = []

    for x, coord in enumerate(coords):
        # on- and off-curve points are defined in
        # the `flags` integer array that are mapped
        # 1:1 to coordinate indices
        on_curve: bool = (flags[x] & FLAG_ON_CURVE) != 0
        # this is a start coordinate if it
        # (1) is the first coordinate in the iterable
        # (2) follows a previous endpoint coordinate
        start_coord: bool = (x == 0) or (coords[x - 1] in endpoint_coordinates)
        # this is an end coordinate if the coordinate tuple is in
        # endpoint_coordinates
        end_coord: bool = coord in endpoint_coordinates
        # cannot be both start and end point
        assert not (end_coord and start_coord)

        if include_implied:
            if not on_curve:
                # there should always be a previous point in the contour
                # if this is *not* an on-curve point
                last_on_curve = (flags[x - 1] & FLAG_ON_CURVE) != 0
                if not last_on_curve:
                    last = coords[x - 1]
                    # get the implied on curve point between two off curve points
                    implied_coordinate = midpoint_between_coordinates(last, coord)
                    new_implied_coordinate = Coordinate(
                        implied_coordinate[0],
                        implied_coordinate[1],
                        oncurve=True,
                        startpoint=False,
                        endpoint=False,
                        implied=True,
                    )
                    # add *new* implied coordinate that was not in the original
                    # coordinate set
                    # set next coordinate attr in the last coordinate if there is one
                    if len(new_coords) > 0 and not new_coords[-1].endpoint:
                        new_coords[-1].set_coord_next(new_implied_coordinate)
                        new_implied_coordinate.set_coord_previous(new_coords[-1])
                    # add the new implied coordinate
                    new_coords.append(new_implied_coordinate)
        # add current coordinate object from this
        # iteration on the original coordinate set
        new_coordinate = Coordinate(
            coord[0],
            coord[1],
            oncurve=on_curve,
            startpoint=start_coord,
            endpoint=end_coord,
            implied=False,
        )
        if len(new_coords) > 0 and not new_coords[-1].endpoint:
            new_coords[-1].set_coord_next(new_coordinate)
            new_coordinate.set_coord_previous(new_coords[-1])
        new_coords.append(new_coordinate)

    return new_coords
