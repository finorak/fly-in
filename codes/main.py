import sys
import json
from typing import Any
from player.player import Player
import pygame
from board.board import Board
from utils.map_parsing import parsing, get_path
from settings import WIDTH, HEIGHT, BACKGROUND_COLOR


class App:
    def __init__(self, args: str | None = None) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fly-in")
        try:
            self.config: dict[str, Any] | None = parsing(
                    get_path(
                        "maps", "easy", "01_linear_path.txt"
                        )
                    )
        except Exception as e:
            print(e)
            print("Aborting...")
            sys.exit(1)
        if self.config is None:
            print("Map Error !!")
            sys.exit(1)
        with open("map.json", "w") as file:
            json.dump(self.config, file, indent=4)
        self.board = Board(self.config, 10, 10)
        self.cell_size = (
                self.board.cell_width, self.board.cell_height
                )
        end_point = self.get_end_point(self.config['hub'])
        x, y = end_point[0]
        end_x, end_y = end_point[1]
        self.players: list[Player] = [Player(
            x,
            y,
            self.cell_size,
            (end_x, end_y),
            "flight_jet.png")
            for _ in range(self.config['nb_drones'])]
        self.running = True

    def get_end_point(self,
                      config: list[dict[str | None, Any]]
                      ) -> list[tuple[int, int]]:
        x: int = -1
        y: int = -1
        end_x: int = -1
        end_y: int = -1
        for hub in config:
            if hub['start']:
                x, y = hub['x'], hub['y']
            if hub['end']:
                end_x, end_y = hub['x'], hub['y']
        return [(x, y), (end_x, end_y)]

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick() / 1000
            self.draw(self.screen, dt)
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

    def draw(self, screen: pygame.Surface, dt: float) -> None:
        screen.fill(BACKGROUND_COLOR)
        self.board.draw(screen, dt)
        self.draw_player(screen, dt)

    def draw_player(self, screen: pygame.Surface, dt: float) -> None:
        for player in self.players:
            player.draw_player(screen, dt)


if __name__ == "__main__":
    app = App()
    app.run()
