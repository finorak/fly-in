from os import listdir, path
from typing import Any, Optional

import pygame
import webcolors
from models.hub_model import HubModel

from utils.map_error import MapError


def get_path(*args: str) -> Any:
    """Getting the absolute path of the
    file
    Parameters:
        args: a list of string to represent the path.
    """
    return path.abspath(path.join(*args))


def load_images(*args: str) -> pygame.Surface:
    """Getting the loaded images.
    Parameters:
        args: a list of string to represent the path
    Returns:
        the loaded image
    """
    return pygame.image.load(get_path(*args))


def load_image_from_dir(state: str) -> list[Any]:
    """We already know where the images
    files are stored, so we use this function
    to avoid repeating this.
    Parameters:
        state: one of 'landing', 'idl', 'wlak'
    Returns:
        a list of available spries
    """
    return [
            load_images(
                'assets', 'img', state, file
                ) for file in listdir(
                    get_path('assets', 'img', state))
            ]


def generate_color(
        color_name: str,
        falback_color: str = "white",
        index: Optional[int] = None) -> Any:
    """Generating the color requested by the metadata.
    Parameters:
        color_name: the name of the color.
        falback_color: in case where the color is not
        valid, we switch back to this.
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


def get_dimension(hubs: dict[str, HubModel]) -> int:
    """Getting the dimension, Just iterating
    over the hubs and get the maximum between
    the x and y for all the hubs
    Parameters:
        hubs: a dict containing all the hub
        represented by teir name.
    Returns:
        the dimension we got.
    """
    sizes: set = set()
    for hub_name in hubs:
        sizes.add(hubs[hub_name].x)
        sizes.add(hubs[hub_name].y)
    x: int = max(list(sizes))
    y: int = -min(list(sizes))
    if x > y:
        return x + 1
    return y + 1
