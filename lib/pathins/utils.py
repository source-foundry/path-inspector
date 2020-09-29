import os
from typing import Union


def is_truetype_font(filepath: Union[bytes, str, "os.PathLike[str]"]) -> bool:
    """Tests that a font has the TrueType file signature of either:
    1) b'\x00\x01\x00\x00'
    2) b'\x74\x72\x75\x65' == 'true'"""
    with open(filepath, "rb") as f:
        file_signature: bytes = f.read(4)

        return file_signature in (b"\x00\x01\x00\x00", b"\x74\x72\x75\x65")
