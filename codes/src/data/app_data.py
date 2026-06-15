from typing import Any

from parser.parsing import Parser
from src.cell import Cell
from src.drone import Drone
from src.connection import Connection
from src.groups.groups import SpriteGroup, SimulationGroup
from utils.helper import load_image_from_dir, load_images


class Data:
    """Class containing all our data, In other
    word a builder class.
    """
    def __init__(self, parser: Parser,
                 groups: list[SpriteGroup | SimulationGroup]) -> None:
        """Constructor for the data clss.
        Parameters:
            parser: class containing the parsed data.
            groups: list of group that control all
                    the associated sprites
        """
        self.parser = parser
        self.cells: list[list[Cell | int]] = []
        self.drones: list[Drone] = []
        self.connections: list[Connection] = []
        self.named_cell: dict[str, Cell] = {}
        self.groups = groups
        self.images: dict[str, Any] = self.load_all_images()

    def create_cells(self) -> None:
        """Creating all the cells, based on the
        data we got from the parsed data.
        """
        # just filling the cells so that we can
        # use it to our need
        for i in range(self.parser.size[0]):
            self.cells.append([])
            for _ in range(self.parser.size[1]):
                self.cells[i].append(0)
        # placing the cell to the correct
        # coordonate
        for hub_name in self.parser.hubs:
            data = self.parser.hubs[hub_name]
            data.x += self.parser.size[2]
            data.y += self.parser.size[3]
            cell: Cell = Cell(**data, size=self.parser.size,
                              groups=self.groups)
            x, y = cell.data.pos
            for group in self.groups:
                group.add(cell)
            self.named_cell[cell.data.name] = cell
            self.cells[x][y] = cell

    def create_connections(self, sprite_group: SpriteGroup) -> None:
        """Creating the connection between the hubs
        """
        for conn in self.parser.conns:
            connection: Connection = Connection(
                self.named_cell[conn.hub_a.name],
                self.named_cell[conn.hub_b.name],
                group=sprite_group,
                max_link_capacity=conn.max_link_capacity
                )
            self.connections.append(connection)

    def create_drones(self) -> None:
        """Creating all the drones and initializing them
        """
        for i in range(1, self.parser.data['nb_drones'] + 1):
            drone: Drone = Drone(
                i, self.named_cell[self.parser.start],
                self.named_cell[self.parser.end],
                self.images, self.groups[0]
                )
            self.drones.append(drone)

    def load_all_images(self) -> dict[str, Any]:
        """Loading all required images from the assets
        folder
        """
        data: dict[str, Any] = {}
        data['background'] = load_images(
                'assets', 'img', 'background',
                'background 1', '1.png')
        data['idl'] = load_image_from_dir('idl')
        data['walk'] = load_image_from_dir('walk')
        data['landing'] = load_image_from_dir('landing')
        return data
