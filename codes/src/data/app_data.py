from typing import Any

from parser.parsing import Parser
from src.cell import Cell
from src.connection import Connection


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
        self.images: dict[str, Any] = {}

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
