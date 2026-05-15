from typing import Any


def get_dimention(hubs: list[dict[str, Any]]) -> tuple[int, int]:
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
