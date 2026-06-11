import pygame


class Drone(pygame.sprite.Sprite):
    def __init__(
            self,
            pos: tuple[int, int],
            image: pygame.Surface,
            *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
