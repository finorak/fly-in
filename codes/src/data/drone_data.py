import pygame
from src.cell import Cell


class DroneData:
    """Drone data container
    """
    def __init__(self, drone_id: int, start_zone: Cell, end_zone: Cell,
                 frames: dict[str, list[pygame.Surface]]
                 ) -> None:
        """Constructor for a drone instance.
        Parameters:
            start_zone: where the drone start
            end_zone: where the simulation end.
            frames: dict containing all the possible
                    state a drone can have
        """
        self.drone_id = f"D{drone_id}"
        self.start_zone = start_zone
        self.end_zone = end_zone
        self.frames = frames
        self.frame_speed: float = 8
        self.speed: float = 100
        self.frame_index: float = 0
        self.state = 'idl'
