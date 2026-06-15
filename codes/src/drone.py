import pygame

from src.cell import Cell


class Drone(pygame.sprite.Sprite):
    """Class for representing the drones
    """
    def __init__(
            self, id: int, start_zone: Cell, end_zone: Cell,
            frames: dict[str, list[pygame.Surface]],
            *groups: pygame.sprite.Group) -> None:
        """Constructor for our drones.
        Parameters:
            start_zone: The start of the done
            end_zone: Where the simulation end
            frames: a dict that contain all the state
                    a drones can have and their frames
                    representation
            groups: to control the sprites
        """
        super().__init__(*groups)
        self.id = f"D{id}"
        self.state = "idl"
        self.frames = frames
        self.image = frames[self.state][0].convert_alpha()
        self.rect = self.image.get_rect(
                bottom=self.set_rect(start_zone, self.image)
                )
        self.start_zone = start_zone
        self.end_zone = end_zone
        self.index: float = 0
        self.speed: float = 5
        self.frame_speed = 5

    def set_rect(self, zone: Cell, image: pygame.Surface) -> int:
        """To avoi warning from mypy we split
        it into this function
        Parameters:
            zone: The zone we want our drone to be centered
            image: the image we want to render
        """
        mask = pygame.mask.from_surface(image)
        visible_rect = mask.get_bounding_rects()[0]
        return zone.rect.top + visible_rect.bottom - image.get_height()

    def update(self, dt: float) -> None:
        """We override the update method from
        the Sprite class, because we want
        animation to our simulation
        Parameters:
            dt: delta time of our simulation
                so that it still have the same
                frames accross diferent device
                even on older oone
        """
        frame_len = len(self.frames[self.state])
        if self.state == "landing" and int(self.index) == frame_len:
            self.image = self.frames[self.state][frame_len - 1]
        else:
            self.index += self.frame_speed * dt
            self.image = self.frames[self.state][int(self.index) % frame_len]
