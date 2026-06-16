import pygame
from settings import HEIGHT, WIDTH

from src.groups.groups import CameraGroup


class GroundSprite(pygame.sprite.Sprite):
    def __init__(self, groups: CameraGroup) -> None:
        super().__init__(groups)
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_frect(center=(WIDTH // 2, HEIGHT // 2))
