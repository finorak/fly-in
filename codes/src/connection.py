import pygame

from src.cell import Cell
from src.groups.groups import SpriteGroup
from settings import LINE_COLOR, LINE_SIZE


class Connection(pygame.sprite.Sprite):
    """Representation of the connection.
    for this class
    """
    def __init__(self, cell_a: Cell, cell_b: Cell,
                 group: SpriteGroup,
                 max_link_capacity: int = 1
                 ) -> None:
        """Constructor for a connection instance.
        Parameters:
            cell_a: a cell instance
            cell_b: a cell instance
            max_link_capacity: how many drones can pass
                                throug this conneciton
                                at the same time.
        """
        super().__init__(group)
        self.cell_a = cell_a
        self.cell_b = cell_b
        self.max_link_capacity = max_link_capacity
        self.image = pygame.Surface(LINE_SIZE)
        self.rect = self.image.get_rect(center=cell_a.rect.center)
        pygame.draw.line(self.image, LINE_COLOR,
                         cell_a.rect.center,
                         cell_b.rect.center)

    def __str__(self) -> str:
        return f"Connecting {self.cell_a.data.name} \
and {self.cell_b.data.name}:\
capacity {self.max_link_capacity}"
