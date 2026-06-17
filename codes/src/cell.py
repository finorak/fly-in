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
            groups: list[SimulationGroup | SpriteGroup], max_drones: int = 1,
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
                name, (x - dimension[2], y - dimension[3]))
        self.image: pygame.Surface = pygame.Surface(
            (CELL_WIDTH, CELL_HEIGHT)
            )
        self.color = color
        self.image.fill(self.color)
        self.rect: pygame.Rect = self.image.get_rect(
            topleft=(x * (CELL_WIDTH + CELL_WIDTH_GAP),
                     y * (CELL_HEIGHT + CELL_HEIGHT_GAP))
            )
        self.neighboors: set[Cell] = set()

    def set_position(self, x: int, y: int) -> tuple[int, int]:
        # TODO: Might remove this function if find best
        # way other than this.
        """Setting the position of the cell so
        that we can accept negative value.
        Parameters:
            x: the x coordinate of the cell.
            y: the y coordinate of the cell.
        Returns:
            the normalized postion
        """
        if x < 0:
            x = self.dimension[0] - x
        if y < 0:
            y = self.dimension[1] - y
        return x, y

    def find_neighboor(self, connections: list[Connection]) -> set['Cell']:
        """Finding the neighboor of this cell,
        Parameters:
            connections: list of connections.
        """
        for conn in connections:
            if conn.cell_a == self and conn.cell_b.data.zone != "blocked":
                self.neighboors.add(conn.cell_b)
        return self.neighboors

    def __str__(self) -> str:
        """How do we want to print this class
        Returns:
            the format we want to represent this class
        """
        return f"{self.data.name} pos: ({self.data.pos}), \
max_drones: {self.data.max_drones}, \
zone: {self.data.zone}, color: {self.color}"
