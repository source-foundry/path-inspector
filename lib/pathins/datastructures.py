from typing import Optional


class Coordinate(object):
    def __init__(
        self,
        x: int,
        y: int,
        oncurve: bool = False,
        startpoint: bool = False,
        endpoint: bool = False,
        implied: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.oncurve = oncurve
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.implied = implied
        self.coord_next: Optional[Coordinate] = None
        self.coord_previous: Optional[Coordinate] = None

    def __str__(self) -> str:
        obj_str = (
            f"Coordinate< ({self.x},{self.y}) oncurve: {self.oncurve}, "
            f"startpoint: {self.startpoint}, endpoint: {self.endpoint}, "
            f"implied: {self.implied} >"
        )
        return obj_str

    def __repr__(self) -> str:
        obj_str = (
            f"Coordinate< ({self.x},{self.y}) oncurve: {self.oncurve}, "
            f"startpoint: {self.startpoint}, endpoint: {self.endpoint}, "
            f"implied: {self.implied} >"
        )
        return obj_str

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.oncurve == other.oncurve
            and self.startpoint == other.startpoint
            and self.endpoint == other.endpoint
            and self.implied == other.implied
        )

    def __ne__(self, other):
        return (
            self.x != other.x
            or self.y != other.y
            or self.oncurve != other.oncurve
            or self.startpoint != other.startpoint
            or self.endpoint != other.endpoint
            or self.implied != other.implied
        )

    def set_coord_next(self, coord: Optional["Coordinate"]) -> None:
        self.coord_next = coord

    def set_coord_previous(self, coord: Optional["Coordinate"]) -> None:
        self.coord_previous = coord
