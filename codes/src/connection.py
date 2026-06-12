import pygame

from src.cell import Cell


class Connection(pygame.sprite.Sprite):
    """Representation of the connection.
    for this class
    """
    def __init__(self, hub_a: Cell,
                 hub_b: Cell, *groups: pygame.sprite.Group,
                 max_link_capacity: int = 1) -> None:
        """Constructor for a connection instance.
        Parameters:
            hub_a: a cell
            hub_b: a cell
            groups: to control the sprites, for this
            i intend to just use line, but with this
            it will be more versatile
            max_link_capacity: how many drones can pass
            throug this conneciton at the same time.
        """
        super().__init__(*groups)
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_link_capacity = max_link_capacity

    def __str__(self) -> str:
        return f"Connecting {self.hub_a.data.name} and {self.hub_b.data.name}:\
capacity {self.max_link_capacity}"
