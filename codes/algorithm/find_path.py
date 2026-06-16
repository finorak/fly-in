from copy import deepcopy

from src.drone import Drone
from src.cell import Cell
from src.connection import Connection


def algorithme(drone: Drone, cells: dict[tuple[int, int], Cell], coonnections: dict[tuple[int, int], Connection]) -> tuple[int, int]:
    """Finding the best next cell to go to
    Parameters:
        drone: the drone that need the best cell \
based on it's current cell
        cells: a dict containing all the cells.
        coonnections: the connections that the current cell \
has if it's utils to us
    Returns:
        a tuple, the position of the next cell
    """
    # TODO: Implementing the algorithme
    ...
