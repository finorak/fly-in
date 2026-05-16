from typing import Any

from board.cell import Cell


def get_dimention(hubs: list[dict[str, Any]]) -> tuple[int, int]:
    """
    Getting the best dimention for the map
    and we pick the maximum of those value
    in the app engine
    """
    rows: int = 0
    cols: int = 0
    for hub in hubs:
        if hub["x"] >= rows:
            rows = hub["x"]
        if hub["y"] >= cols:
            cols = hub["y"]
    return rows + 1, cols + 1


def get_end_point(
        config: list[dict[str | None, Any]]
        ) -> list[tuple[int, int]]:
    """
    getting endpoint of the config we
    recieved from config
    """
    x: int = -1
    y: int = -1
    end_x: int = -1
    end_y: int = -1
    for hub in config:
        if hub["start"]:
            x, y = hub["x"], hub["y"]
        if hub["end"]:
            end_x, end_y = hub["x"], hub["y"]
    return [(x, y), (end_x, end_y)]


def arrange_cells(cells: list[list[Cell]]) -> dict[str, Cell]:
    """
    Arranging the cells structure
    this is only used to establishe the connexion
    as it is a lot of work to verify the it each time
    using a for loop, but here we just look for it's key
    and then render it into the table and still
    able to verify if the cell is currently inside
    or not
    """
    data: dict[str, Cell] = {}
    for row in cells:
        for cell in row:
            data[cell.name.strip()] = cell
    return data
