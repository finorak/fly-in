from typing import Any

import pygame
from settings import LINE_COLOR
from src.groups.groups import SpriteGroup


class Connection(pygame.sprite.Sprite):
    """Representation of the connection.
    for this class
    """
    def __init__(self,
                 cell_a: Any, cell_b: Any,
                 group: SpriteGroup, conn_name: str,
                 max_link_capacity: int = 1
                 ) -> None:
        """Constructor for a connection instance.
        Parameters:
            cell_a: a cell instance
            cell_b: a cell instance
            group: the group that control our sprite.
            max_link_capacity: how many drones can pass
                                throug this conneciton
                                at the same time.
        """
        super().__init__(group)
        self.cell_a = cell_a
        self.cell_b = cell_b
        self.conn_name: str = conn_name
        self.dron_traversing: int = 0
        self.max_link_capacity = max_link_capacity
        self.network = True
        self.group = group

    def _update_line(self) -> None:
        """Update the line drawing and position based on cell positions.
        This follows the camera offset automatically since the sprite
        is drawn relative to the screen during custom_draw.
        """
        start_pos = self.cell_a.rect.center
        end_pos = self.cell_b.rect.center
        min_x = min(start_pos[0], end_pos[0])
        min_y = min(start_pos[1], end_pos[1])
        max_x = max(start_pos[0], end_pos[0])
        max_y = max(start_pos[1], end_pos[1])
        width = max(max_x - min_x, 10)
        height = max(max_y - min_y, 10)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        local_start_x = start_pos[0] - min_x
        local_start_y = start_pos[1] - min_y
        local_end_x = end_pos[0] - min_x
        local_end_y = end_pos[1] - min_y
        pygame.draw.line(
                self.image, LINE_COLOR,
                (local_start_x, local_start_y),
                (local_end_x, local_end_y), 2)
        self.rect = self.image.get_frect(topleft=(min_x, min_y))

    def update(self, dt: float = 0) -> None:
        """Update line position to follow cells.
        Parameters:
            dt: delta time
        """
        self._update_line()

    def __str__(self) -> str:
        return f"Connecting {self.cell_a.data.name} \
and {self.cell_b.data.name}:\
capacity {self.max_link_capacity}"
