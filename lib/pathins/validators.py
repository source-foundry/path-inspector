import os
import sys
from typing import Union

from fontTools.ttLib import ttFont  # type: ignore

from .utils import is_truetype_font


def validate_fontpath(fontpath: Union[bytes, str, "os.PathLike[str]"]) -> None:
    if not os.path.isfile(fontpath):
        sys.stderr.write(
            f"error: {str(fontpath)} does not appear to be a file{os.linesep}"
        )
        sys.exit(1)
    if not is_truetype_font(fontpath):
        sys.stderr.write(
            f"error: {str(fontpath)} does not appear to be a TTF format font{os.linesep}"
        )
        sys.exit(1)


def validate_glyph_in_font(glyph_name: str, tt_font: ttFont.TTFont) -> None:
    try:
        tt_font["glyf"][glyph_name]  # type: ignore
    except Exception:
        sys.stderr.write(
            f"error: Failed to open glyph '{glyph_name}'. "
            f"Does it exist in the font?{os.linesep}"
        )
        sys.exit(1)
