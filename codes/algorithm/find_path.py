from src.cell import Cell
from src.connection import Connection
from src.drone import Drone


def algorithme(
        drone: Drone,
        cells: dict[tuple[int, int], Cell],
        conections: list[Connection]
        ) -> tuple[int, int]:
    """Finding the best next cell to go to
    Parameters:
        drone: the drone that need the best cell \
based on it's current cell
        cells: a dict containing all the cells.
        conections: the connections that the current cell \
has if it's utils to us
    Returns:
        a tuple, the position of the next best cell
        it can be the same as the drone's current
        pos
    """
    return 0, 0
