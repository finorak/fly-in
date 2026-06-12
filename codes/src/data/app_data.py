from typing import Any

from parser.parsing import Parser
from src.cell import Cell
from src.connection import Connection
from utils.helper import load_image_from_dir, load_images


class Data:
    """Class containing all our data, In other
    word a builder class.
    """
    def __init__(self, parser: Parser) -> None:
        """Constructor for the data clss.
        Parameters:
            parser: class containing the parsed data.
        """
        self.parser = parser
        self.cells: list[Cell] = []
        self.connections: list[Connection] = []
        self.organized: dict[str, Cell] = {}
        self.images: dict[str, Any] = self.load_all_images()

    def create_cells(self) -> None:
        """Creating all the cells, based on the
        data we got from the parsed data.
        """
        for hub_name in self.parser.hubs:
            data = self.parser.hubs[hub_name]
            cell: Cell = Cell(**data, size=self.parser.size)
            self.organized[cell.data.name] = cell
            self.cells.append(cell)

    def create_connections(self) -> None:
        """Creating the connection between the hubs
        """
        for conn in self.parser.conns:
            connection: Connection = Connection(
                    self.organized[conn.hub_a.name],
                    self.organized[conn.hub_b.name],
                    max_link_capacity=conn.max_link_capacity
                    )
            self.connections.append(connection)

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
