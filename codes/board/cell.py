from typing import Any


class Cell:
    def __init__(
        self,
        row: int,
        col: int,
        cell_width: float,
        cell_height: float,
        color: Any = None,
    ) -> None:
        self.row = row
        self.col = col
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.color = color
