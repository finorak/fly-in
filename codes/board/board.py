from typing import Any

import pygame
from board.cell import Cell
from settings import (
    BACKGROUND_COLOR,
    BLUE,
    HEIGHT,
    WIDTH,
    ZONE_COLOR,
    ZONE_COSTS,
)


class Board:
    def __init__(self, config: dict[str, Any],
                 rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.cell_size = (WIDTH / self.rows, HEIGHT / self.cols)
        self.config: dict[str, Any] = config
        self.cells: list[list[Cell]] = [
            [
                self.get_cell(i, j, *self.cell_size)
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

    def get_cell(
        self, row: int, col: int, cell_width: float, cell_height: float
    ) -> Cell:
        """
        TODO: Add a fixed color for the cell that isn't a hub
        """
        cell = Cell(row, col, self.cell_size, "_")
        for hub in self.config["hub"]:
            if hub["x"] == row and hub["y"] == col:
                cell.name = hub["name"]
                cell.zone = hub["metadata"]["zone"]
                cell.zone_cost = ZONE_COSTS[cell.zone]
                cell.max_drones = hub["metadata"]["max_drones"]
                color: str | Any = hub["metadata"]["color"]
                if color is None:
                    color = BLUE
                cell.color = color.strip()
                break
            cell.color = BACKGROUND_COLOR
        return cell

    def draw_board(self, screen: pygame.Surface, dt: float) -> None:
        for row in range(self.cols):
            for col in range(self.rows):
                cell = self.cells[row][col]
                try:
                    pygame.draw.rect(
                        screen,
                        cell.color,
                        (
                            (
                                row * self.cell_size[0],
                                col * self.cell_size[1]),
                            (self.cell_size[0] // 1, self.cell_size[1] // 1),
                        ),
                    )
                except ValueError as e:
                    print(e)
                    cell.color = ZONE_COLOR[cell.zone]
                    pygame.draw.rect(
                        screen,
                        cell.color,
                        (
                            (
                                row * self.cell_size[0],
                                col * self.cell_size[1]),
                            (self.cell_size[0] // 1, self.cell_size[1] // 1),
                        ),
                    )
