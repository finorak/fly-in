from typing import Any, Optional

import webcolors
from parser.map_error import MapError


def generate_color(
        color_name: str,
        falback_color: str = "white",
        index: Optional[int] = None) -> Any:
    """Generating the color requested by the metadata.
    Parameters:
        color_name: the name of the color.
        index: the line where to use if there was
        an error in the metadata.
    Returns:
        the hex representation of that specific
        color_name
    """
    if not color_name.isalpha():
        raise MapError(f"Line {index}: color name isn't a string")
    try:
        hex_color = webcolors.name_to_hex(color_name)
        return hex_color
    except ValueError:
        if index is None:
            return webcolors.name_to_hex(falback_color)
        raise MapError(f"Line {index}: Color invalid")
