from os import listdir, path
from typing import Any, Optional

import pygame
import webcolors
from models.hub_model import HubModel

from utils.errors import MapError


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


def generate_color(color_name: str,
                   index: Optional[int] = None,
                   falback_color: str = "white") -> Any:
    """Generating the color requested by the metadata.
    Parameters:
        color_name: color we want to extract
        index: index at which we got the metadata
        falback_color: what color to use in case the color_name
                        isn't correct
    Returns:
        hex representation of the color we extracted
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


def get_dimension(hubs: dict[str, HubModel]) -> tuple[int, int, int, int]:
    """Getting the dimension, Just iterating
    over the hubs and get the maximum between
    the x and y for all the hubs
    Parameters:
        hubs: a dict containing all the hub
            represented by teir name.
    Returns:
        tuple: that contain the dimension,
                the min of x and y.
    """
    x_sizes: set[int] = set()
    y_sizes: set[int] = set()
    for hub_name in hubs:
        x_sizes.add(hubs[hub_name].x)
        y_sizes.add(hubs[hub_name].y)
    x_min: int = min(list(x_sizes))
    x_max: int = max(list(x_sizes))
    y_min: int = min(list(y_sizes))
    y_max: int = max(list(y_sizes))
    x: int = x_max if x_max > -x_min else -x_min
    y: int = y_max if y_max > -y_min else -y_min
    if x_min == -x:
        x = x ** 2
    if y_min == -y:
        y = y ** 2
    return x + 1, y + 1, x_min, y_min


def get_correct_coordinate(
        size: tuple[int, int],
        x: int, y: int) -> tuple[int, int]:
    """Getting the correct coordonate based
    on the size
    Parameters:
        size: the size we use as bases
        x: the x coordonate of the point
        y: the y coordonate of thhe point
    Returns:
        a tuple that represent the correct coordonate.
    ```
    >>> pos = get_correct_coordinate((4, 1), -3, 0)
    >>> (1, 0)
    ```
    """
    if x < 0:
        x = size[0] + x
    if y < 0:
        y = size[1] + y
    return x, y


def is_numeric(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
