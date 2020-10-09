import os
import sys
from typing import Dict, Sequence, Text, Tuple

from .datastructures import Coordinate

ansicolors: Dict[Text, Text] = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "BRIGHT_BOLD_CYAN": "\033[1;96m",
    "WHITE": "\033[37m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m",
}

bold_start: Text = ansicolors["BOLD"]
green_start: Text = ansicolors["GREEN"]
red_start: Text = ansicolors["RED"]
cyan_start: Text = ansicolors["CYAN"]
bright_cyan_start: Text = ansicolors["BRIGHT_BOLD_CYAN"]
reset: Text = ansicolors["RESET"]

if sys.stdout.isatty():
    IS_A_TTY = True
else:
    IS_A_TTY = False


def bold_text(text: str, nocolor: bool = False) -> str:
    """
    Returns bold text ANSI escape code text string
    """
    if not nocolor and IS_A_TTY:
        return f"{bold_start}{text}{reset}"
    else:
        return text


def cyan_text(text: str, nocolor: bool = False) -> str:
    """
    Returns cyan ANSI escape code colored text string
    """
    if not nocolor and IS_A_TTY:
        return f"{cyan_start}{text}{reset}"
    else:
        return text


def cyan_bright_text(text: str, nocolor: bool = False) -> str:
    """
    Returns cyan ANSI escape code colored text string
    with bold weight
    """
    if not nocolor and IS_A_TTY:
        return f"{bright_cyan_start}{text}{reset}"
    else:
        return text


def green_text(text: str, nocolor: bool = False) -> str:
    """
    Returns green ANSI escape code colored text string
    """
    if not nocolor and IS_A_TTY:
        return f"{green_start}{text}{reset}"
    else:
        return text


def red_text(text: str, nocolor: bool = False) -> str:
    """
    Returns red ANSI escape code colored text string
    """
    if not nocolor and IS_A_TTY:
        return f"{red_start}{text}{reset}"
    else:
        return text


def report_header(header: str, nocolor: bool = False) -> str:
    header_len = len(header) + 1
    divider_char = "-"
    if not nocolor and IS_A_TTY:
        header_string = (
            f"{divider_char * header_len}{os.linesep}"
            f"{bright_cyan_start}{header}{reset}{os.linesep}"
            f"{divider_char * header_len}"
        )
    else:
        header_string = (
            f"{divider_char * header_len}{os.linesep}"
            f"{header}{os.linesep}"
            f"{divider_char * header_len}"
        )
    return header_string


# def overlap_result(glyphname: str, test_pass: bool, nocolor: bool = False) -> str:
#     # color
#     if not nocolor and IS_A_TTY:
#         if test_pass:
#             result_pre = f"[ {red_start}{glyphname}{reset} ]: "
#         else:
#             result_pre = f"[ {green_start}{glyphname}{reset} ]: "
#     else:
#         result_pre = f"[ {glyphname} ]: "
#     # test pass indicator
#     if test_pass:
#         result = result_pre + "Yes"
#     else:
#         result = result_pre + "No"
#     return result


def direction_result(
    glyphname: str,
    direction_clockwise: bool,
    contours: int,
    components_with_transforms: Sequence[Tuple] = [],
    nocolor: bool = False,
) -> str:
    if not nocolor and IS_A_TTY:
        if contours == 0:
            return f"[ {bright_cyan_start}{glyphname}{reset} ]: no contours"
        if direction_clockwise:
            return (
                f"[ {bright_cyan_start}{glyphname}{reset} ]: "
                f"clockwise"
                f"{_transformed_component(components_with_transforms)}"
            )
        else:
            return (
                f"[ {bright_cyan_start}{glyphname}{reset} ]: "
                f"counter-clockwise"
                f"{_transformed_component(components_with_transforms)}"
            )
    else:
        if contours == 0:
            return f"[ {glyphname} ]: no contours"
        if direction_clockwise:
            return (
                f"[ {glyphname} ]: clockwise"
                f"{_transformed_component(components_with_transforms)}"
            )
        else:
            return (
                f"[ {glyphname} ]: counter-clockwise"
                f"{_transformed_component(components_with_transforms)}"
            )


def _transformed_component(components_with_transforms: Sequence[Tuple]) -> str:
    if len(components_with_transforms) > 0:
        left_pad = " " * 10
        components_string = f"{os.linesep}"
        for x, component in enumerate(components_with_transforms):
            component_glyphname = component[0]
            component_transform = component[1]
            components_string += (
                f"{left_pad}with component '{component_glyphname}' transform: "
                f"{component_transform}"
            )
            if x + 1 < len(components_with_transforms):
                # add newline unless this is the last component in the list
                components_string += f"{os.linesep}"
        return components_string
    else:
        return ""


def segment_line(
    coord1: Coordinate, coord2: Coordinate, distance: float, nocolor: bool = False
) -> str:
    if not nocolor and IS_A_TTY:
        # color coord1 start and end points
        if coord1.startpoint:
            coordinates1 = f"{green_start}({coord1.x},{coord1.y}){reset}"
        elif coord1.endpoint:
            coordinates1 = f"{red_start}({coord1.x},{coord1.y}){reset}"
        else:
            coordinates1 = f"({coord1.x},{coord1.y})"

        # color coord2 start points (end of curve)
        if coord2.startpoint:
            coordinates2 = f"{green_start}({coord2.x},{coord2.y}){reset}"
        else:
            coordinates2 = f"({coord2.x},{coord2.y})"

        return (
            f"{coordinates1} {coordinates2}: "
            f"{cyan_bright_text('LINE')} {round(distance, 2):.2f} units"
        )
    else:
        return (
            f"({coord1.x},{coord1.y}) ({coord2.x},{coord2.y}): "
            f"LINE {round(distance, 2):.2f} units"
        )


def segment_quadratic_curve(
    coord1: Coordinate,
    coord2: Coordinate,
    coord3: Coordinate,
    distance: float,
    nocolor: bool = False,
) -> str:
    if not nocolor and IS_A_TTY:
        if coord1.startpoint:
            coordinates1 = f"{green_start}({coord1.x},{coord1.y}){reset}"
        elif coord1.endpoint:
            coordinates1 = f"{red_start}({coord1.x},{coord1.y}){reset}"
        else:
            coordinates1 = f"({coord1.x},{coord1.y})"

        if coord2.endpoint:
            coordinates2 = f"{red_start}({coord2.x},{coord2.y}){reset}"
        else:
            coordinates2 = f"({coord2.x},{coord2.y})"

        if coord3.startpoint:
            coordinates3 = f"{green_start}({coord3.x},{coord3.y}){reset}"
        elif coord3.endpoint:
            coordinates3 = f"{red_start}({coord3.x},{coord3.y}){reset}"
        else:
            coordinates3 = f"({coord3.x},{coord3.y})"

        return (
            f"{coordinates1} {coordinates2} {coordinates3}: "
            f"{cyan_bright_text('QCURVE')} {round(distance, 2):.2f} units"
        )
    else:
        return (
            f"({coord1.x},{coord1.y}) ({coord2.x},{coord2.y}) ({coord3.x},{coord3.y}): "
            f"QCURVE {round(distance, 2):.2f} units"
        )


def segment_total_distance(distance: float, nocolor: bool = False) -> str:
    if not nocolor and IS_A_TTY:
        return f"{bold_text('Total')}: {round(distance, 2):.2f} units"
    else:
        return f"Total: {round(distance, 2):.2f} units"
