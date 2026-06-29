import pygame
from parser.parsing import Parser
from src.drone import Drone
from settings import TITLE, WIN_SIZE
from src.data.data import AppData
from src.groups.groups import SpriteGroup
from utils.errors import MapError
from utils.helper import cell_lead_to_goal


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
        if visual:
            self.init_gui()
        self.sprite_group: SpriteGroup = SpriteGroup()
        self.data = AppData(parser, [self.sprite_group])

    def init_gui(self) -> None:
        """Initializing gui,
        THis will be only used, if visual is True
        """
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.SCALED)
        pygame.display.set_caption(TITLE)

    def init(self) -> None:
        """We avoid lunching any function from
        the init method, so that's why we
        use this fuinction to do that task
        by calling it from the one that need this class
        """
        self.data.images['background'] = pygame.transform.scale(
                self.data.images['background'], WIN_SIZE)
        self.data.create_cells()
        self.data.create_connections(self.sprite_group)
        self.data.create_drones()
        if not cell_lead_to_goal(
                self.data.start_zone[0],
                self.data.end_zone):
            raise MapError("Map error, Can't solve it")

    def run(self, drones: list[Drone]) -> None:
        """The function to run the program.
        Parameters:
            drones: list of drone.
        """
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            self.move_drones(drones, dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
                if event.type == pygame.MOUSEWHEEL:
                    self.sprite_group.zoom_camera(event, dt)
            self.update(dt)
            self.draw(self.screen, dt)
        pygame.quit()

    def move_drones(self, drones: list[Drone], dt: float) -> None:
        """FUnction used to move all drones to the
        end zone.
        Parameters:
            drones: list of drone to move.
            dt: delta time.
        """

    def update(self, dt: float) -> None:
        """update what we've got so far
        on the screen.
        Parameters:
            dt: delta time
        """
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
        screen.fill("white")
        self.sprite_group.custom_draw(
                screen,
                self.data.images['background'], dt
                )
