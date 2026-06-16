from typing import Any

from settings import ZONES


class CellData:
    """Builder class for a cell instance.
    """
    def __init__(
            self, max_drones: int, zone: str,
            name: str, pos: tuple[int, int]) -> None:
        """Constructor for a cell class.
        To avoid the class to contain a lot of
        attribute.
        Parameters:
            max_drones: how many drones a hub
                        can have.
            zone: the zone.
            name: the name of the hub.
            pos: the position of the hub.
        """
        self.max_drones: int = max_drones
        self.zone: str = zone
        self.turn_cost: int = ZONES[self.zone]['cost']
        self.name: str = name
        self._drones: dict[str, list[Any]] = {}
        self.pos: tuple[int, int] = pos
