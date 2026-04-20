import sys
import json
from typing import Any
from player.player import Player
import pygame
from board.board import Board
from utils.map_parsing import parsing, get_path
from settings import WIDTH, HEIGHT, BACKGROUND_COLOR


class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("App")
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
        self.players: list[Player] = [Player(
            self.config['start_hub']['x'],
            self.config['start_hub']['y'],
            self.cell_size,
            (self.config['end_hub']['x'], self.config['end_hub']['y']),
            "flight_jet.png")
            for _ in range(self.config['nb_drones'])]
        self.running = True

    def run(self) -> None:
        while self.running:
            self.draw(self.screen)
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

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        self.board.draw(screen)
        self.draw_player(screen)

    def draw_player(self, screen: pygame.Surface) -> None:
        for player in self.players:
            player.draw_player(screen)


if __name__ == "__main__":
    app = App()
    app.run()
