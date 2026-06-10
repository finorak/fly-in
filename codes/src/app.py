import pygame
from codes.models.hub import HubModel
from parser.parsing import Parser
from settings import BG_COLOR, HEIGHT, TITLE, WIDTH


class App:
    """The main app for our application
    """
    def __init__(self, parser: Parser) -> None:
        """Constructor for an app instance
        """
        self.parser = parser
        self.screen = pygame.display.set_mode(
                (WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

    def _init(self, hubs: list[HubModel]) -> list[str]:
        for hub in hubs:
            ...
        return []

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
        self.screen.fill(BG_COLOR)
        pass
