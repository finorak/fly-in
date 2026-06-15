class CellData:
    """Builder class for a cell instance.
    """
    def __init__(
            self, max_drones: int, zone: str,
            name: str, pos: tuple[int, int]) -> None:
        """Constructor for a cell class.
        To avoid the class to contain a lot of
        attribute.
        """
        self.max_drones = max_drones
        self.zone = zone
        self.name = name
        self.index = 0
        self._drone_stationed = 0
        self.pos = pos
