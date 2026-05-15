from typing import Any
import pygame
from board.cell import Cell


class Connection:
    """
    The conection between the two hub,
    into a class so that it become more
    customizable oin the future
    """

    def __init__(
        self, hub_1: Cell, hub_2: Cell, color: Any,
        link_capacity: int = 1
    ) -> None:
        self.hub_1 = hub_1
        self.hub_2 = hub_2
        self.color = color
        self.link_capacity = link_capacity

    def draw_connection(self, surface: pygame.Surface) -> None:
        pygame.draw.line(
            surface,
            self.color,
            self.get_pos(self.hub_1),
            self.get_pos(self.hub_2),
            width=10,
        )

    def get_pos(self, cell: Cell) -> tuple[float, float]:
        width, height = cell.cell_size
        x: float = cell.col * width + width / 2
        y: float = cell.row * height + height / 2
        return (x, y)
