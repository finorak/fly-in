from typing import Optional

import pygame

from src.data.cell_data import CellData


class Cell(pygame.sprite.Sprite):
    """Cell class, we use to represent a
    cell.
    """
    def __init__(
            self,
            x: int,
            y: int,
            name: str,
            size: int,
            *groups: pygame.sprite.Group,
            max_drones: int = 1,
            color: str = 'white',
            zone: str = 'normal',
            image: Optional[pygame.Surface] = None
            ) -> None:
        """Constructor for a cell instance.
        Parameters:
            pas: the position of the cell.
            groups: for the sprites to be used
            correctly we store them in a groups
            image: the image to be shown to represent
            our cell.
        """
        super().__init__(*groups)
        self.data = CellData(max_drones, zone, name, color, image)
        self.size = size
        self.x = x
        self.y = y
        self.image = pygame.Surface(self.set_position(x, y))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def set_position(self, x: int, y: int) -> tuple[int, int]:
        """Setting the position of the cell so
        that we can accept negative value.
        Parameters:
            x: the x coordinate of the cell.
            y: the y coordinate of the cell.
        Returns:
            the normalized postion
        """
        if x < 0:
            x = self.size - x
        if y < 0:
            y = self.size - y
        return x, y

    def __str__(self) -> str:
        return f"{self.data.name} => pos: ({self.x}, \
{self.y}), max_drones: {self.data.max_drones}, \
zone: {self.data.zone}, color: {self.data.color}"
