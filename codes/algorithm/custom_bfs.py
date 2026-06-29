"""
TODO: THE OUTPUT IS SOMEWHAT BROKEN, NEED TO FIX:
THAT IS THE MOST IMPORTANT TASK FOR THIS

"""



from collections import deque
from typing import Any

from utils.helper import join_name, quit_app
import sys
from src.drone import Drone
from src.cell import Cell
from src.connection import Connection


class Algo:
    def __init__(
        self,
        drones: list[Drone],
        cells: dict[tuple[int, int], Cell],
        connecitons: dict[str, Connection],
    ) -> None:
        self.drones = drones
        self.cells = cells
        self.connections = connecitons
        self.drones_cpy = self.drones.copy()

    def cell_cost_to_reach_goal(self, current_cell: Cell, end_zone: Cell) -> float:
        neighboors = deque([current_cell])
        came_from: dict[Cell, Cell | None] = {current_cell: None}
        visited: set[Cell] = set()
        while neighboors:
            current = neighboors.popleft()
            if current == end_zone:
                break
            visited.add(current)
            for neighboor in current.neighboors:
                if neighboor in visited:
                    continue
                came_from[neighboor] = current
        if end_zone not in came_from:
            return float("inf")
        current = end_zone
        cost: float = 0
        while current is not None:
            cost += current.data.turn_cost
            current = came_from[current]
        return cost

    def can_go(
        self,
        current_cell: Cell,
        end_cell: Cell,
        connection: Connection | None,
        neighboors: set[Cell],
    ) -> bool:
        if current_cell == end_cell:
            return True
        current_best = self.cell_cost_to_reach_goal(current_cell, end_cell)
        other_neighboors: list[Cell] = [
                cell for cell in neighboors if cell != current_cell
            ]
        if connection and connection.is_full():
            for cell in other_neighboors:
                new_best = self.cell_cost_to_reach_goal(cell, end_cell)
                if new_best <= current_best:
                    return False
        if current_cell.is_full():
            other_neighboors: list[Cell] = [
                cell for cell in neighboors if cell != current_cell
            ]
            for cell in other_neighboors:
                # TODO: learning why this doesn't
                # work if <=, we got a large number
                # of turn
                new_best = self.cell_cost_to_reach_goal(cell, end_cell)
                if new_best <= current_best:
                    return False
        return True

    def algorithme(
        self, current_drone: Drone, connections: dict[str, Connection]
    ) -> list[Cell]:
        current_zone = current_drone.current_zone
        end_zone = current_drone.data.end_zone
        visited: set[Cell] = set()
        came_frome: dict[Any, Cell | None] = {current_zone: None}
        neighboors = deque([current_zone])
        start_neighboors_len = len(current_zone.neighboors)
        counter = 0
        starter = True
        while neighboors:
            quit_app()
            if counter > start_neighboors_len:
                starter = False
            current = neighboors.popleft()
            if current == end_zone:
                break
            visited.add(current)
            current_neighboors = current.neighboors
            counter += 1
            hubs: list[Cell] = []
            for neighboor in current_neighboors:
                if neighboor in visited:
                    continue
                # Descision making if cell where
                # to be full of connection full
                connection_name = join_name(current, neighboor)
                connection = connections.get(connection_name)
                if starter and not self.can_go(
                    neighboor, end_zone, connection, current_neighboors
                ):
                    continue
                # end of descision making
                came_frome[neighboor] = current
                hubs.append(neighboor)
            neighboors.extend(
                sorted(
                    hubs,
                    key=lambda cell: (
                        0 if cell.data.zone == "priority" else 1,
                        self.cell_cost_to_reach_goal(cell, end_zone),
                    ),
                )
            )
        if end_zone not in came_frome:
            return []
        paths: list[Cell] = []
        current = end_zone
        while current is not None:
            quit_app()
            paths.append(current)
            current = came_frome[current]
        paths.reverse()
        return paths[1:]

    def solve(self) -> None:
        turn_counter: int = 0
        while self.drones:
            current_turn: list[str] = []
            for drone in self.drones[:]:
                end_zone = drone.data.end_zone
                if drone.restricted_next_zone:
                    drone.current_conneciton.increment_drones_by = -1
                    drone.current_zone = drone.restricted_next_zone
                    drone.current_zone.increment_drones_by = 1
                    drone.current_conneciton = None
                    drone.restricted_next_zone = None
                    current_turn.append(f"{drone}-{drone.current_zone}")
                    continue
                paths = self.algorithme(drone, self.connections)
                if not paths:
                    continue
                next_hub = paths[0]
                if next_hub.is_full() and next_hub != end_zone:
                    continue
                connection_name = join_name(drone.current_zone, next_hub)
                connection = self.connections[connection_name]
                if connection.is_full():
                    continue
                if next_hub.data.zone == "restricted":
                    drone.restricted_next_zone = next_hub
                    drone.current_conneciton = connection
                    drone.current_zone.increment_drones_by = -1
                    connection.increment_drones_by = 1
                    current_turn.append(f"{drone}-{connection}")
                    continue
                drone.current_zone.increment_drones_by = -1
                drone.current_zone = next_hub
                drone.current_zone.increment_drones_by = 1
                if drone.current_zone == end_zone:
                    self.drones.remove(drone)
                current_turn.append(f"{drone}-{drone.current_zone}")
            turn = " ".join(current_turn)
            turn_counter += 1
            print(turn)
        print()
        print(f"Turn count: {turn_counter}", file=sys.stderr)
