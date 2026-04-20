from typing import Any


class Cell:
    def __init__(
        self,
        row: int,
        col: int,
        cell_width: float,
        cell_height: float,
        name: str | None = None,
        color: Any = None,
        zone: str = "normal",
        zone_cost: int = 1,
        max_drones: int = 1
    ) -> None:
        self.row = row
        self.col = col
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.color = color
        self.zone = zone
        self.max_drones = max_drones
        self.name = name
        self.zon_cost = zone_cost
