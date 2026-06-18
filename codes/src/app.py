import pygame
from algorithm.find_path import algorithme
from parser.parsing import Parser
from settings import TITLE, WIN_SIZE
from src.data.app_data import AppData
from src.groups.groups import CameraGroup, SimulationGroup, SpriteGroup
from utils.errors import MapError
from utils.helper import start_lead_to_goal


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
        self.camera_group: CameraGroup = CameraGroup()
        self.data = AppData(parser, [self.sprite_group, self.simulation_group])
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.SCALED)
        pygame.display.set_caption(TITLE)

    def _init(self) -> None:
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
        if not start_lead_to_goal(
                self.data.start_zone[0],
                self.data.end_zone):
            raise MapError("Map error, Can't solve it")

    def run(self) -> None:
        """The function to run the program.
        """
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            self.solve(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
                # if event.type == pygame.MOUSEWHEEL:
                #     self.sprite_group.zoom_camera(event, dt)
            self.update(dt)
            self.draw(self.screen, dt)
        pygame.quit()

    def solve(self, dt: float = 0) -> None:
        """Solving the maze,
        Iterating over all the drones
        and trying to find the best solution
        Parameters:
            dt: delta time used for animation
        """
        for drone in self.data.drones:
            if algorithme(drone, self.data.cells, self.data.connections):
                drone.move_drone(dt)

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
