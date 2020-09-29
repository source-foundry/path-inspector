import os
import sys
from typing import Dict, Text

ansicolors: Dict[Text, Text] = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "LIGHT_CYAN": "\033[1;36m",
    "WHITE": "\033[37m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m",
}

green_start: Text = ansicolors["GREEN"]
red_start: Text = ansicolors["RED"]
cyan_start: Text = ansicolors["CYAN"]
light_cyan_start: Text = ansicolors["LIGHT_CYAN"]
reset: Text = ansicolors["RESET"]


def path_header(header: str, nocolor=False) -> str:
    header_len = len(header) + 1
    divider_char = "-"
    if not nocolor and sys.stdout.isatty():
        header_string = (
            f"{divider_char * header_len}{os.linesep}"
            f"{light_cyan_start}{header}{reset}{os.linesep}"
            f"{divider_char * header_len}"
        )
    else:
        header_string = (
            f"{divider_char * header_len}{os.linesep}"
            f"{header}{os.linesep}"
            f"{divider_char * header_len}"
        )
    return header_string


def overlap_result(glyphname: str, test_pass: bool, nocolor=False) -> str:
    # color
    if not nocolor and sys.stdout.isatty():
        if test_pass:
            result_pre = f"[ {red_start}{glyphname}{reset} ]: "
        else:
            result_pre = f"[ {green_start}{glyphname}{reset} ]: "
    else:
        result_pre = f"[{glyphname}]: "
    # test pass indicator
    if test_pass:
        result = result_pre + "Yes"
    else:
        result = result_pre + "No"
    return result


def direction_result(
    glyphname: str, direction_clockwise: bool, contours: int, nocolor=False
) -> str:
    if not nocolor and sys.stdout.isatty():
        if contours == 0:
            return f"[ {light_cyan_start}{glyphname}{reset} ]: no contours"
        if direction_clockwise:
            return f"[ {light_cyan_start}{glyphname}{reset} ]: clockwise"
        else:
            return f"[ {light_cyan_start}{glyphname}{reset} ]: counter-clockwise"
    else:
        if contours == 0:
            return f"[ {glyphname} ]: no contours"
        if direction_clockwise:
            return f"[ {glyphname} ]: clockwise"
        else:
            return f"[ {glyphname} ]: counter-clockwise"
