from argparse import ArgumentParser, Namespace
from os import listdir, path
from typing import Any, Optional

import pygame
import webcolors
from models.hub_model import HubModel
from utils.errors import MapError


def get_args() -> Namespace:
    """Using argparse, we can add
    another argument without modifying
    to many codes, just adding a few lines
    of codes.
    """
    parser: ArgumentParser = ArgumentParser(
            description="A drone simulation app",
            usage="uv run python -m codes --input [file]")
    parser.add_argument(
            "--input", type=str, help="Map file",
            default="maps/easy/01_linear_path.txt"
            )
    parser.add_argument(
        "--max", type=int,
        default=44
    )
    parser.add_argument(
            "--visual", type=bool, help="To show or not",
            default=False
            )
    return parser.parse_args()


def get_path(*args: str) -> Any:
    """Getting the absolute path of the
    file
    Parameters:
        args: a list of string to represent the path.
    """
    return path.abspath(path.join(*args))


def load_image(*args: str) -> pygame.Surface:
    """Getting the loaded images.
    Parameters:
        args: a list of string to represent the path
    Returns:
        the loaded image
    ```
    >>> load_images('assets', 'img', 'walk')
    ```
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
            load_image(
                'assets', 'img', state, file
                ) for file in listdir(
                    get_path('assets', 'img', state)
                    )
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
    >>> red_hex_color = genrate_color("red")
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


def duplicate_position(hub_models: list[HubModel], hub: HubModel) -> bool:
    """Verifying if the cell's position is
    already in the list
    Parameters:
        hub_models: a dict of hub_model
        hub: the hub to verify
    Returns:
        boolean value
    """
    for model in hub_models:
        if model.x == hub.x and model.y == hub.y:
            return True
    return False


def cell_lead_to_goal(
        current_zone: Any,
        end_zone: Any,
        ) -> bool:
    """In case someone where to input
    a map that doesn't lead to the end goal,
    we recursively go in each hub neighboor of
    the current cell
    Parameters:
        current_cell: the current cell we are in
        end_zone: the goal
        solving: This tell us our current state \
if we are solving it or just looking if the maze
can be solved or not
    Returns:
        boolean value.
    """
    stack = [current_zone]
    visited: set = set()
    while stack:
        cell = stack.pop()
        if cell in visited:
            continue
        if cell == end_zone:
            return True
        visited.add(cell)
        lst = list(cell.neighboors)
        stack.extend(lst)
        # for neighboor in stack:
        #     if neighboor == current_zone:
        #         return False
    return False
    

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
        x += 1
    if y_min == -y:
        y += 1
    if x_min < 0:
        x_min = -x_min
    if y_min < 0:
        y_min = -y_min
    return x + 1, y + 1, x_min, y_min


def join_name(cell_a: Any, cell_b: Any) -> str:
    """This seem to be repetitive function
    so we englobe it into this function
    Parameters:
        cell_a: a Cell
        cell_b: a Cell
    Returns:
        the string representing the connection
        between those two cells
    """
    return "-".join([cell_a.data.name, cell_b.data.name])


def is_numeric(value: str) -> bool:
    """A simple function that check if
    a value is numerical or not
    because the original, numeric
    done't tell us if the vlau is a negative
    or not
    Parameters:
        value: the value to verify
    ```
    >>> is_numeric("5")
        True
    >>> is_numeric("-5")
        True
    >>> is_numeric(" -5")
        False
    ```
    """
    try:
        int(value)
        return True
    except ValueError:
        return False
