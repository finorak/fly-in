import pygame
from settings import (
    CELL_HEIGHT, CELL_HEIGHT_GAP,
    CELL_WIDTH, CELL_WIDTH_GAP, ZONES
)
from src.connection import Connection
from src.groups.groups import SpriteGroup
from utils.helper import generate_color


class CellData:
    """Builder class for a cell instance.
    """
    def __init__(
            self, max_drones: int, zone: str,
            name: str, pos: tuple[int, int], win_pos: tuple[int, int]) -> None:
        """Constructor for a cell class.
        To avoid the class to contain a lot of
        attribute.
        Parameters:
            max_drones: how many drones a hub
                        can have.
            zone: the zone.
            name: the name of the hub.
            pos: the position of the hub.
        """
        self.max_drones: int = max_drones
        self.zone: str = zone
        self.turn_cost: int = ZONES[self.zone]['cost']
        self.name: str = name
        self._drones: dict[str, list['Cell']] = {}
        self.win_pos = win_pos
        self.pos: tuple[int, int] = pos


class Cell(pygame.sprite.Sprite):
    """Cell class, we use to represent a
    cell.
    """
    def __init__(
        self, x: int, y: int, name: str,
        dimension: tuple[int, int, int, int],
        groups: list[SpriteGroup], win_pos: tuple[int, int],
        image: pygame.Surface, max_drones: int = 1,
        color: str = 'white', zone: str = 'normal'
    ) -> None:
        """Constructor for a cell instance.
        Parameters:
            x: x coordinate of the cell
            y: y coordinate of the cell
            name: the name of the cell \
dimension: the dimension
            zone: zone of the cell one of 'normal', 'restricted' \
'blocked', 'priority'
            groups: for the sprites to be used \
correctly we store them in a groups
            color: the color of the cell, by default \
we use white
            image: the image to be shown to represent \
our cell.
            max_drones: how many drone a cell can have.
        """
        super().__init__(*groups)
        self.dimension: tuple[int, int, int, int] = dimension
        self.data = CellData(
            max_drones, zone,
            name, (x - dimension[2], y - dimension[3]), win_pos=win_pos
        )
        self.image: pygame.Surface = pygame.Surface(
            (CELL_WIDTH, CELL_HEIGHT)
        )
        self._nb_drones: int = 0
        self.color = generate_color(
            color_name=color, falback_color=ZONES[self.data.zone]['color']
        )
        # self.image.fill(self.color)
        self.rect: pygame.Rect = self.image.get_rect(
            topleft=(x * (CELL_WIDTH + CELL_WIDTH_GAP),
                     y * (CELL_HEIGHT + CELL_HEIGHT_GAP))
        )
        self.camera_offset: pygame.math.Vector2 = pygame.math.Vector2()
        self.neighboors: list[Cell] = []

    def update(self, dt: float) -> None:
        """For the hover effect, but for now,
        we'll use this for debugging.
        Parameters:
            dt: delta time
        """
        self.image.fill(self.color)
        ...

    def find_neighboor(
        self, connections: dict[str, Connection]
    ) -> list['Cell']:
        """Finding the neighboor of this cell, based
        on the connections
        Parameters:
            connections: dict representing the connections.
        Returns:
            set of connections
        """
        for conn in connections:
            if conn.startswith(self.data.name):
                next_cell = connections[conn].cell_b
                if next_cell.data.zone == "blocked":
                    continue
                if next_cell == self or next_cell in self.neighboors:
                    continue
                self.neighboors.append(next_cell)
            elif conn.endswith(self.data.name):
                prev_cell = connections[conn].cell_a
                if prev_cell.data.zone == 'blocked':
                    continue
                if prev_cell == self or prev_cell in self.neighboors:
                    continue
                self.neighboors.append(prev_cell)
        return self.neighboors

    @property
    def increment_drones_by(self) -> int:
        """Instead of using the private attribute
        we use this property.
        """
        return self._nb_drones

    @increment_drones_by.setter
    def increment_drones_by(self, value: int) -> None:
        """Instead of using the private attribute
        we use this property.
        """
        self._nb_drones += value

    def is_full(self) -> bool:
        """Verifying if the cell is full
        or not.
        Returns:
            True if full else False
        """
        return bool(self.increment_drones_by >= self.data.max_drones)

    def __str__(self) -> str:
        """How do we want to print this class
        Returns:
            the format we want to represent this class
        """
        return f"{self.data.name}"
