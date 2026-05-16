"""
The engine that power the drones
"""

import json
from typing import Any

import pygame
from board.board import Board
from board.cell import Cell
from board.connection import Connection
from player.player import Player
from settings import BACKGROUND_COLOR, FRAME_LIMIT, HEIGHT, TITLE, WIDTH
from utils.map_utils import arrange_cells, get_dimention, get_end_point


class App:
    def __init__(self, config: dict[str, Any]) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.config = config
        with open("map.json", "w") as f:
            data = json.dumps(self.config, indent=4)
            f.write(data)
        dimention: tuple[int, int] = get_dimention(self.config['hub'])
        self.size: int = max(dimention)
        self.board = Board(self.config, self.size, self.size)
        self.cell_size = self.board.cell_size
        end_point = get_end_point(self.config['hub'])
        end_x, end_y = end_point[1]
        self.players: list[Player] = [Player(
            *end_point[0],
            self.cell_size,
            self.board.cells[end_x][end_y],
            "flight_jet.png")
            for _ in range(self.config['nb_drones'])]
        self.connections: list[Connection] = self.init_connection()
        self.running = True

    def run(self) -> None:
        """
        THe function that run the flying
        simulator
        """
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick() / FRAME_LIMIT
            mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
            x = mouse_pos[0] // self.cell_size[0]
            y = mouse_pos[1] // self.cell_size[1]
            self.draw(self.screen, self.connections, dt)
            self.hover_effect(int(x), int(y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONUP:
                    pos: tuple[int, int] = pygame.mouse.get_pos()
                    row: int = int(pos[0] // self.cell_size[0])
                    col: int = int(pos[1] // self.cell_size[1])
                    name = self.board.cells[row][col].name
                    if name is None:
                        break
                    print(name, (row, col))
            pygame.display.update()
        pygame.quit()

    # TODO: make this work after finishing the project
    def hover_effect(self, x: int, y: int) -> None:
        """
        Putting an hover effect: details about the cell
        how many cells or in it, and so on...
        """
        if not 0 <= x < self.size and 0 <= y < self.size:
            return None
        if self.board.cells[x][y].name is None:
            return None

    def draw(self, screen: pygame.Surface,
             connections: list[Connection],
             dt: float) -> None:
        """
        Drawing onto the screen
        """
        screen.fill(BACKGROUND_COLOR)
        self.board.draw_board(screen, dt)
        self.draw_connection(screen, connections)
        self.draw_player(screen, dt)

    def draw_player(self, screen: pygame.Surface, dt: float) -> None:
        """
        Drawing player onto screen...
        """
        for player in self.players:
            player.draw_player(screen, dt)

    def init_connection(self) -> list[Connection]:
        """
        Initializing all the connection
        so that we can view it on the screen
        """
        connections: list[Connection] = []
        arranged: dict[str, Cell] = arrange_cells(self.board.cells)
        for conn in self.config['connection']:
            try:
                connection = Connection(arranged[conn['a']],
                                    arranged[conn['b']],
                                    conn['metadata']['color'],
                                    conn['metadata']['max_link_capacity'])
                connections.append(connection)
            except Exception as e:
                print(e)
                continue
        return connections

    def draw_connection(self, screen: pygame.Surface,
                        connections: list[Connection]) -> None:
        for con in connections:
            con.draw_connection(screen)
