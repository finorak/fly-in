from typing import Any


class Plan:
    def __init__(self,
                 x: int,
                 y: int,
                 end_pos: tuple[int, int]) -> None:
        self.x = x
        self.y = y
        self.end_pos = end_pos

    def find_path(self) -> Any:
        pass