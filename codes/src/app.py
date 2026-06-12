import pygame
from parser.parsing import Parser
from settings import HEIGHT, TITLE, WIDTH

from src.cell import Cell
from src.data.app_data import Data


class App:
    """The main app for our application
    """
    def __init__(self, parser: Parser, visual: bool = False) -> None:
        """Constructor for an app instance
        Parameters:
            parser: class containing the parsed data.
        """
        pygame.init()
        self.data = Data(parser)
        self.screen = pygame.display.set_mode(
                (WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.cells: list[Cell] = []

    def _init(self) -> None:
        """We avoid lunching any function from
        the init method, so that's why we
        use this fuinction to do that task
        by calling it from the one that need this class
        """
        self.data.create_cells()
        self.data.create_connections()
        self.data.images['background'] = pygame.transform.scale(
                self.data.images['background'], (WIDTH, HEIGHT)
                ).convert_alpha()
        for cell in self.data.cells:
            print(cell)
        print("#" * 50)
        for conn in self.data.connections:
            print(conn)

    def run(self) -> None:
        """The function to run the program.
        """
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            self.draw(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            pygame.display.update()
        pygame.quit()

    def draw(self, dt: float) -> None:
        """Drawing the sprites, images, etc
        into the window.
        Parameters:
            dt: delta time of each frames, so
            that it doesn't glich even on
            older pc.
        """
        self.screen.blit(self.data.images['background'])
