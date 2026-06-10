from typing import Any

import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: tuple[int, int], *groups: Any) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
