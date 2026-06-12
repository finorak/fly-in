import pygame


class Drone(pygame.sprite.Sprite):
    """Class for representing the drones
    """
    def __init__(
            self,
            pos: tuple[int, int],
            image: pygame.Surface,
            *groups: pygame.sprite.Group) -> None:
        """Constructor for our drones.
        Parameters:
            pos: the position of the drone.
            image: the image to use for the drones
            groups: to control the sprites
        """
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
