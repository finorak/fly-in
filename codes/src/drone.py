from typing import Any
import pygame

from src.data.drone_data import DroneData
from src.cell import Cell


class Drone(pygame.sprite.Sprite):
    """Class for representing the drones"""

    def __init__(
        self,
        drone_id: int,
        start_zone: Cell,
        end_zone: Cell,
        frames: dict[str, list[pygame.Surface]],
        *groups: pygame.sprite.Group,
    ) -> None:
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
        self.frames: dict[str, list[pygame.Surface]] = frames
        self.data: DroneData = DroneData(
                drone_id, start_zone, end_zone, frames)
        self.image: pygame.Surface = frames[self.data.state][0].convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(
            bottom=self.set_rect(start_zone, self.image)
        )
        self.current_zone: Cell = start_zone
        self.move: bool = False

    def set_rect(self, zone: Cell, image: pygame.Surface) -> Any:
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
        if self.move:
            self.data.state = "walk"
        if self.current_zone == self.data.end_zone:
            self.data.state = "landing"
            self.move = False
        frame_len = len(self.frames[self.data.state])
        if self.data.state == "landing" and int(
                self.data.frame_index) == frame_len:
            self.image = self.frames[self.data.state][frame_len - 1]
        else:
            self.data.frame_index += self.data.frame_speed * dt
            self.image = self.frames[self.data.state][
                int(self.data.frame_index) % frame_len
            ]

    def __str__(self) -> str:
        return f"{self.data.drone_id}"
