from typing import Any
import pygame
import random
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
        self.direction = random.choice([-1, 1])
        self.angle: float = self.direction
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

    def get_angle(self, dt: float) -> float:
        self.angle += (90 * dt) % 360
        return self.angle

    def find_path(self) -> Any:
        pass
