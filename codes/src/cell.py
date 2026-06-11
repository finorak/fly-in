from typing import Optional
import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(
            self,
            pos: tuple[int, int],
            *groups: pygame.sprite.Group,
            image: Optional[pygame.Surface] = None
            ) -> None:
        super().__init__(*groups)
        self.pos = pos
        self.image = pygame.Surface(self.pos)
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.center = pos
