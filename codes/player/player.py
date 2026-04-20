from typing import Any
import pygame
from utils.map_parsing import get_path


class Player:
    def __init__(self,
                 x: int,
                 y: int,
                 size: tuple[float, float],
                 end_pos: tuple[int, int],
                 image_name: Any) -> None:
        self.x = x
        self.y = y
        self.end_pos = end_pos
        self.size = size
        self.image = pygame.transform.scale(
                pygame.image.load(get_path(
                    "assets", "img", image_name
                    )), (self.size[0] // 2, self.size[1] // 2)
                ).convert_alpha()

    def find_path(self) -> Any:
        pass

    def draw_player(self, screen: pygame.Surface) -> None:
        img_rect = self.image.get_rect()
        img_rect.center = (
                self.x * self.size[0] + self.size[0] // 2,
                self.y * self.size[1] + self.size[1] // 2,
                )
        screen.blit(self.image, img_rect)
