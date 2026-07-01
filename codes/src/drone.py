from typing import Any

import pygame
from settings import CELL_HEIGHT_GAP
from src.cell import Cell
from src.connection import Connection
import random


class DroneData:
    """Drone data container
    """
    def __init__(
        self, drone_id: int, start_zone: Cell,
        end_zone: Cell, frames: dict[str, list[pygame.Surface]]
    ) -> None:
        """Constructor for a drone instance.
        Parameters:
            start_zone: where the drone start
            end_zone: where the simulation end.
            frames: dict containing all the possible
                    state a drone can have
        """
        self.drone_id = f"D{drone_id}"
        self.start_zone: Cell = start_zone
        self.end_zone: Cell = end_zone
        self.frames: dict[str, list[pygame.Surface]] = frames
        self.frame_speed: float = 8
        self.speed: float = 600  # AT SCHOOL
        # self.speed: float = 300  # at home
        self.frame_index: float = random.randint(0, len(frames))
        self.state: str = 'idl'


class Drone(pygame.sprite.Sprite):
    """Class for representing the drones"""

    def __init__(
            self, drone_id: int, start_zone: Cell,
            end_zone: Cell, frames: dict[str, list[pygame.Surface]],
            *groups: Any,
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
        self.image: pygame.Surface = frames[self.data.state][0]
        self.rect: pygame.Rect = self.image.get_rect(
            center=self.place_drone(start_zone)
        )
        self.current_zone: Cell = start_zone
        self.current_conneciton: Connection | Any = None
        self.paths: list[Cell] = []
        self.restricted_next_zone: Cell | Any = None
        self.move: bool = False
        self.wait: bool = False
        self.target_index: int = 0

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
        frame_len = len(self.frames[self.data.state])
        self.data.frame_index += self.data.frame_speed * dt
        self.image = self.frames[self.data.state][
            int(self.data.frame_index) % frame_len
        ]

    def place_drone(self, zone: Cell) -> Any:
        """Placing the drone to the place we want to put it.
        Parameters:
            zone: the zone to place the drone.
        """
        return zone.rect.center - pygame.math.Vector2((0, CELL_HEIGHT_GAP / 4))

    def move_drone(self, dt: float) -> bool:
        """Moving the drone, after finding the
        path, where paths is a list of cell
        Parameters:
            dt: delta time
        """
        if not self.paths:
            return True
        if self.target_index >= len(self.paths):
            return True
        target_zone = self.paths[self.target_index]
        target_x, target_y = self.place_drone(target_zone)
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 1:
            self.data.state = "walk"
            t = min(self.data.speed * dt, distance)
            self.rect.x += (dx / distance) * t
            self.rect.y += (dy / distance) * t
            return False
        self.current_zone = target_zone
        self.data.state = "idl"
        return True

    def __str__(self) -> str:
        """How to represent the drone
        when printing it.
        """
        return f"{self.data.drone_id}"
