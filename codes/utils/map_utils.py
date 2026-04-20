from typing import Any


def get_dimention(hubs: list[dict[str, Any]]) -> tuple[int, int]:
    rows: int = 0
    cols: int = 0
    for hub in hubs:
        if hub['x'] >= rows:
            rows = hub['x']
        if hub['y'] >= cols:
            cols = hub['y']
    return rows + 1, cols + 1
