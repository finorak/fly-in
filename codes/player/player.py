import math
from typing import Any

import pygame
from board.cell import Cell
from utils.parsing import get_path


class Player:
    def __init__(self,
                 x: int,
                 y: int,
                 size: tuple[float, float],
                 end_hub: Cell,
                 image_name: Any) -> None:
        self.x = x
        self.y = y
        self.end_hub = end_hub
        self.size = size
        self.angle: float = 0
        self.image = pygame.transform.scale(
                pygame.image.load(get_path(
                    "assets", "img", image_name
                    )), (self.size[0] // 2, self.size[1] // 2)
                ).convert_alpha()

    def draw_player(self, screen: pygame.Surface, dt: float) -> None:
        new_img = pygame.transform.rotate(
                self.image, self.get_angle(dt)
                )
        img_rect = new_img.get_rect()
        img_rect.center = (
                self.x * self.size[0] + self.size[0] // 2,
                self.y * self.size[1] + self.size[1] // 2,
                )
        screen.blit(new_img, img_rect)

    def get_angle(self, dt: float, next_cell: Cell | None = None) -> float:
        if next_cell is None:
            next_cell = self.end_hub
        self.angle = math.degrees(
                math.atan2(
                    -(next_cell.row - self.y),
                    next_cell.col - self.x
                    ))
        return self.angle

    def find_path(self,
                  cells: list[list[Cell]],
                  start_pos: tuple[int, int] = (0, 0)
                  ) -> bool:
        # start_cell = cells[start_pos[0]][start_pos[1]]
        return True
