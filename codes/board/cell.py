from typing import Any


class Cell:
    def __init__(
        self,
        row: int,
        col: int,
        size: tuple[float, float],
        name: str,
        color: Any = None,
        zone: str = "normal",
        zone_cost: int = 1,
        max_drones: int = 1,
    ) -> None:
        self.row = row
        self.col = col
        self.cell_size = size
        self.color = color
        self.zone = zone
        self.max_drones = max_drones
        self.name = name
        self.zone_cost = zone_cost
        self.full = False
        self.nb_drones: list[Any] = []

    def add_drone(self, player: Any) -> None:
        if len(self.nb_drones) >= self.max_drones:
            self.full = True
        if self.full:
            return None
        self.nb_drones.append(player)

    def remove_drone(self) -> None:
        if self.nb_drones:
            self.nb_drones.pop(0)

    def get_pos(self) -> tuple[int, int]:
        return (self.row, self.col)
