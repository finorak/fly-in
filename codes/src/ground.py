import pygame
from settings import WIN_SIZE
from src.groups.groups import CameraGroup


class GroundSprite(pygame.sprite.Sprite):
    def __init__(self, groups: CameraGroup) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        self.rect = self.image.get_frect(center=(
            WIN_SIZE[0] // 2, WIN_SIZE[1] // 2)
        )
