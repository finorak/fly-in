from typing import Any

import pygame
from settings import CELL_HEIGHT_GAP
from src.cell import Cell
from src.data.drone_data import DroneData


class Drone(pygame.sprite.Sprite):
    """Class for representing the drones"""

    def __init__(
            self, drone_id: int, start_zone: Cell,
            end_zone: Cell, frames: dict[str, list[pygame.Surface]],
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
        self.image: pygame.Surface = frames[self.data.state][0]
        self.rect: pygame.Rect = self.image.get_rect(
            center=self.place_drone(start_zone)
        )
        self.current_zone: Cell = start_zone
        self.paths: list[Cell] = []
        self.restricted_next_zone: Cell | Any = None
        self.can_move: bool = True
        self.move: bool = False
        self.wait: bool = False
        self.found_path: bool = False

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
        # if self.move:
        #     self.data.state = "walk"
        # if self.current_zone == self.data.end_zone:
        #     self.data.state = "landing"
        #     self.move = False
        frame_len = len(self.frames[self.data.state])
        # if self.data.state == "landing" and int(
        #         self.data.frame_index) == frame_len:
        #     self.image = self.frames[self.data.state][frame_len - 1]
        # else:
        self.data.frame_index += self.data.frame_speed * dt
        self.image = self.frames[self.data.state][
            int(self.data.frame_index) % frame_len
        ]

    def place_drone(self, zone: Cell) -> Any:
        return zone.rect.center - pygame.math.Vector2((0, CELL_HEIGHT_GAP / 4))

    def move_drone(self, dt: float) -> None:
        """Moving the drone, after finding the
        path, where paths is a list of cell
        Parameters:
            dt: delta time
        """
        if not self.paths or self.current_zone == self.data.end_zone:
            return
        target_zone = self.paths[0]
        target_x, target_y = self.place_drone(target_zone)
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            t = min(self.data.speed * dt, distance)
            self.rect.x = self.rect.x + (dx / distance) * t
            self.rect.y = self.rect.y + (dy / distance) * t
        else:
            self.current_zone = target_zone

    def __str__(self) -> str:
        """How to represent the drone
        when printing it.
        """
        return f"{self.data.drone_id}"
