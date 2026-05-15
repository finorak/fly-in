from typing import Any

import pygame
from board.cell import Cell
from player.player import Player
from settings import END_ZONE_COLOR


class Connection:
    """
    The conection between the two hub,
    into a class so that it become more
    customizable oin the future
    """

    def __init__(
        self, hub_1: Cell, hub_2: Cell,
        color: Any, link_capacity: int = 1
    ) -> None:
        self.hub_1 = hub_1
        self.hub_2 = hub_2
        self.color = color
        if not self.color:
            self.color = END_ZONE_COLOR
        self.start = self.get_pos(self.hub_1)
        self.end = self.get_pos(self.hub_2)
        self.link_capacity = link_capacity
        self.player_traversing: list[Player] = []

    def draw_connection(self, screen: pygame.Surface) -> None:
        pygame.draw.line(
            screen,
            self.color,
            self.start,
            self.end,
            width=10,
        )
        self.draw_circle(screen, self.start, END_ZONE_COLOR)
        self.draw_circle(screen, self.end, END_ZONE_COLOR)

    def get_pos(self, cell: Cell) -> tuple[float, float]:
        width, height = cell.cell_size
        x: float = cell.row * width + width / 2
        y: float = cell.col * height + height / 2
        return (x, y)

    def draw_circle(self, screen: pygame.Surface,
                    center: tuple[float, float],
                    color: Any) -> None:
        pygame.draw.circle(screen, color, center, 15)

    def is_free(self) -> bool:
        return len(self.player_traversing) < self.link_capacity
