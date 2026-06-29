from collections import deque
from typing import Any

from utils.helper import join_name, quit_app
import sys
from src.connection import Connection


class CustomBFS:
    def __init__(
        self,
        drones: list[Any],
        cells: dict[tuple[int, int], Any],
        connecitons: dict[str, Connection],
    ) -> None:
        self.drones = drones
        self.cells = cells
        self.connections = connecitons
        self.drones_cpy: list[Any] = []

    def cell_cost_to_reach_goal(
            self, current_cell: Any, end_zone: Any
            ) -> float:
        neighboors = deque([current_cell])
        came_from: dict[Any, Any | None] = {current_cell: None}
        visited: set[Any] = set()
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
        current_cell: Any,
        end_cell: Any,
        connection: Connection | None,
        neighboors: set[Any],
    ) -> bool:
        if current_cell == end_cell:
            return True
        current_best = self.cell_cost_to_reach_goal(current_cell, end_cell)
        other_neighboors: list[Any] = [
                cell for cell in neighboors if cell != current_cell
            ]
        if connection and connection.is_full():
            for cell in other_neighboors:
                new_best = self.cell_cost_to_reach_goal(cell, end_cell)
                if new_best <= current_best:
                    return False
        if current_cell.is_full():
            for cell in other_neighboors:
                new_best = self.cell_cost_to_reach_goal(cell, end_cell)
                if new_best < current_best:
                    return False
        return True

    def algorithme(
        self, current_drone: Any, connections: dict[str, Connection]
    ) -> list[Any]:
        """The algorithme we use to find the best path based on the current
        zone of the drone.
        At each step of the drone, we loo, for the best
        next cell, from there.
        Parameters:
            current_zone: the drone that need to find the next path.
            connections: the connections, we use this to get
            the current conneciton of the zone and it's neighboor
        Returns:
            list of path.
        """
        current_zone = current_drone.current_zone
        end_zone = current_drone.data.end_zone
        visited: set[Any] = set()
        came_frome: dict[Any, Any | None] = {current_zone: None}
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
            hubs: list[Any] = []
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
        paths: list[Any] = []
        current = end_zone
        while current is not None:
            quit_app()
            paths.append(current)
            current = came_frome[current]
        paths.reverse()
        return paths[1:]

    def solve(self) -> None:
        """Just an api that communicate with algorithme.
        We iterate the list of drones, till there is no
        drone anymore.
        and at each step, we get the paths we got from
        algorithme, and take the first value in that list
        if there is any, it might be empty if it still didn't
        found a path for the current zone of the drone.
        move the drone to that next cell, and so on
        till it reach end zone.
        """
        turn_counter: int = 0
        while self.drones:
            current_turn: list[str] = []
            for drone in self.drones[:]:
                end_zone = drone.data.end_zone
                if drone.restricted_next_zone:
                    drone.current_conneciton.increment_drones_by = -1
                    drone.current_zone = drone.restricted_next_zone
                    drone.current_conneciton = None
                    drone.restricted_next_zone = None
                    current_turn.append(f"{drone}-{drone.current_zone}")
                    continue
                paths = self.algorithme(drone, self.connections)
                if not paths:
                    continue
                next_hub = paths[0]
                connection_name = join_name(drone.current_zone, next_hub)
                connection = self.connections[connection_name]
                # the drone can't do anything at this point,
                # it wait a turn
                if connection.is_full() or (
                        next_hub.is_full() and next_hub != end_zone):
                    continue
                if next_hub.data.zone == "restricted":
                    drone.restricted_next_zone = next_hub
                    next_hub.increment_drones_by = 1
                    drone.current_conneciton = connection
                    drone.current_zone.increment_drones_by = -1
                    connection.increment_drones_by = 1
                    current_turn.append(f"{drone}-{connection}")
                    drone.paths.append(next_hub)
                    continue
                drone.current_zone.increment_drones_by = -1
                drone.current_zone = next_hub
                drone.current_zone.increment_drones_by = 1
                drone.paths.append(next_hub)
                if drone.current_zone == end_zone:
                    self.drones_cpy.append(drone)
                    self.drones.remove(drone)
                current_turn.append(f"{drone}-{drone.current_zone}")
            turn = " ".join(current_turn)
            turn_counter += 1
            print(turn)
        print(f"\nTurn count: {turn_counter}", file=sys.stderr)
