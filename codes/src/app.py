import pygame
from parser.parsing import Parser
from settings import HEIGHT, TITLE, WIDTH
from src.groups.groups import SpriteGroup, SimulationGroup
from src.cell import Cell
from src.data.app_data import Data


class App:
    """The main app for our application
    """
    def __init__(self, parser: Parser, visual: bool = True) -> None:
        """Constructor for an app instance
        Parameters:
            parser: class containing the parsed data.
            visual: whever to show the visualisation
                    or not, by default we see
        """
        pygame.init()
        self.sprite_group: SpriteGroup = SpriteGroup()
        self.simulation_group: SimulationGroup = SimulationGroup()
        self.data = Data(parser, [self.sprite_group, self.simulation_group])
        self.screen = pygame.display.set_mode(
                (WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.cells: list[list[Cell]] = []

    def _init(self) -> None:
        """We avoid lunching any function from
        the init method, so that's why we
        use this fuinction to do that task
        by calling it from the one that need this class
        """
        self.data.create_cells()
        self.data.create_connections(self.sprite_group)
        self.data.images['background'] = pygame.transform.scale(
                self.data.images['background'], (WIDTH, HEIGHT)
                )
        self.data.create_drones()

    def run(self) -> None:
        """The function to run the program.
        """
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            self.update(dt)
            self.draw(self.screen, dt)
        pygame.quit()

    def update(self, dt: float) -> None:
        pygame.display.update()
        self.sprite_group.update(dt)

    def draw(self, screen: pygame.Surface, dt: float) -> None:
        """Drawing the sprites, images, etc
        into the window.
        Parameters:
            screen: where to render
            dt: delta time of each frames, so
                that it doesn't glich even on
                older pc.
        """
        self.screen.blit(self.data.images['background'])
        self.sprite_group.custom_draw(screen, dt)
