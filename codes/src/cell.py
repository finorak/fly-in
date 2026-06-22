import pygame
from settings import CELL_HEIGHT, CELL_HEIGHT_GAP, CELL_WIDTH, CELL_WIDTH_GAP
from src.connection import Connection
from src.data.cell_data import CellData
from src.groups.groups import SimulationGroup, SpriteGroup


class Cell(pygame.sprite.Sprite):
    """Cell class, we use to represent a
    cell.
    """
    def __init__(
            self, x: int, y: int, name: str,
            dimension: tuple[int, int, int, int],
            groups: list[SimulationGroup | SpriteGroup],
            win_pos: tuple[int, int], image: pygame.Surface,
            max_drones: int = 1, color: str = 'white',
            zone: str = 'normal'
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
                name, (x - dimension[2], y - dimension[3]), win_pos=win_pos)
        self.image: pygame.Surface = pygame.Surface(
            (CELL_WIDTH, CELL_HEIGHT)
            )
        self._nb_drones: int = 0
        self.color = color
        self.image.fill(self.color)
        self.rect: pygame.Rect = self.image.get_rect(
            topleft=(x * (CELL_WIDTH + CELL_WIDTH_GAP),
                     y * (CELL_HEIGHT + CELL_HEIGHT_GAP))
            )
        self.camera_offset: pygame.math.Vector2 = pygame.math.Vector2()
        self.neighboors: set[Cell] = set()

    def update(self, dt: float) -> None:
        """For the hover effect, but for now,
        we'll use this for debugging.
        Parameters:
            dt: delta time
        """
        ...

    def find_neighboor(
            self, connections: dict[str, Connection]
            ) -> set['Cell']:
        """Finding the neighboor of this cell,
        Parameters:
            connections: list of connections.
        """
        for conn in connections:
            if conn.startswith(self.data.name):
                next_cell = connections[conn].cell_b
                if next_cell.data.zone == "blocked":
                    continue
                self.neighboors.add(next_cell)
        return self.neighboors

    @property
    def increment_drones_by(self) -> int:
        return self._nb_drones

    @increment_drones_by.setter
    def increment_drones_by(self, value: int) -> None:
        self._nb_drones += value
    
    def is_full(self) -> bool:
        return self.increment_drones_by >= self.data.max_drones

    def __str__(self) -> str:
        """How do we want to print this class
        Returns:
            the format we want to represent this class
        """
        return f"{self.data.name}"
#         return f"{self.data.name} pos: ({self.data.pos}), \
# max_drones: {self.data.max_drones}, \
# zone: {self.data.zone}, color: {self.color}"
