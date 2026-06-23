"""
IDEA: USING A* TO FIND THE BEST MOVE
AFTER FINDING THE BEST MOVE, WE VERIFY THOSE
POINT BELLOW:
    - DOES THE NEXT CELL CAN STILL OCCUPY
      ANOTHER CELL ?
    - CAN THE CONNECTION TO THAT CELL STILL
      HAVE ROOM FOR THE CURRENT TURN ?
AFTER ANSWERING THOSE QUESTION WE GO FOR THE
NEXT APPROACE:
    - BECAUSE IT'S A TURN BASE PATH FINDING
      THE FIRST DRONE WILL ALWAYS BE THE PRIORITY
      SO THAT AFTER IT FOUND THE BEST NEXT CELL
      WE INCREMENT THE NUMBER OF CELLS INSIDE THE
      CELL IT FOUND AND ALSO THE CONNECTION THAT LEAD
      TO THAT CELL
IMPORTANT:
        EACH CELL SHOULD HAVE A DICTIONARY THAT
        CONTAIN THE CONNECTION TO THE NEXT CELL IT'S
        CONNECTED TO
"""


from queue import PriorityQueue
import sys
from typing import Any

from src.cell import Cell
from src.connection import Connection
from src.drone import Drone
from utils.helper import cell_lead_to_goal, join_name


class Turn:
    def __init__(
        self, drones: list[Drone], cells: dict[tuple[int, int], Cell],
        connections: dict[str, Connection]
        ) -> None:
        self.turns: list[Cell | Connection] | Any = None
        self.drones = drones
        self.cells = cells
        self.connections = connections
        self.temp_cells: list[Drone] = []

    def h(self, current_zone: Cell, end_zone: Cell) -> Any:
        """Getting the herestic of the function.
        We do so by calculating the cost of each
        turn
        Parameters:
            current_zone: the current zone to calculate
            end_zone: the end zone for our simulation
        Returns:
            the herestic value
        """
        return current_zone.data.turn_cost - end_zone.data.turn_cost


    def algorithme(
            self, drone: Drone,
            cells: dict[tuple[int, int], Cell],
            connections: dict[str, Connection]
            ) -> list[Cell]:
        """Finding the best path to go to.
        Parameters:
            drone: the drone that need the best cell \
    based on it's current cell
            cells: a dict containing all the cells.
            connections: the connections that the current cell \
    has if it's utils to us
        Returns:
            boolean value that determin if we found \
    the path or not
        """
        count = 0
        open_set: PriorityQueue = PriorityQueue()
        current_zone = drone.current_zone
        end_zone = drone.data.end_zone
        open_set.put((self.h(current_zone, end_zone), count, current_zone))
        came_from: dict[Cell, Cell] = {}
        g_score = {cells[pos]: float("inf") for pos in cells}
        g_score[current_zone] = 0
        f_score: dict[Cell, float] = {cells[pos]: float("inf") for pos in cells}
        f_score[current_zone] = self.h(current_zone, end_zone)
        open_set_hash: set = {current_zone}
        while not open_set.empty():
            current: Cell = open_set.get()[2]
            open_set_hash.remove(current)
            if current == end_zone:
                return list(came_from)
            for _, neighboor in enumerate(list(current.neighboors)):
                if not cell_lead_to_goal(neighboor, end_zone):
                    continue
                # # AVOIDING PATH THAT LEAD TO DEAD END
                if neighboor in drone.paths:
                    continue
                # FIND ANOTHER PATH; THIS ONE IS FULL
                conn_name = join_name(current, neighboor)
                connection = connections[conn_name]
                # Can't go to that cell
                if connection.is_full() or (neighboor.is_full() and neighboor != end_zone):
                    continue
                # might as well this information later on
                # but for now, w'll just comment till
                # we find the use of it
                temp_g_score = g_score[current] + current.data.turn_cost
                if neighboor.data.zone == "priority":
                    temp_g_score = -float("inf")
                if temp_g_score <= g_score[neighboor]:
                    came_from[neighboor] = current
                    g_score[neighboor] = temp_g_score
                    f_score[neighboor] = temp_g_score + self.h(neighboor, end_zone)
                    if neighboor.data.zone == "priority":
                        f_score[neighboor] = -float("inf")
                    if neighboor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighboor], count, neighboor))
                        open_set_hash.add(neighboor)
        return list(came_from)

    def solve(self) -> int:
        """Solving the maze,
        Iterating over all the drones
        and trying to find the best solution
        Parameters:
            drones: a list of drones.
            cells: a list of cells.
            connections: list of connections
        """
        turn_counter = 0
        while self.drones:
            drone_turns: list[str] = []
            for drone in self.drones[:]:
                if drone.restricted_next_zone:
                    drone.current_zone.increment_drones_by = -1
                    drone.current_conneciton.increment_drones_by = -1
                    drone.current_zone = drone.restricted_next_zone
                    drone.restricted_next_zone = None
                    continue
                # SEARCHING PATH FOR THE CURRENT
                # ZONE THE DRONE IS IN
                paths = self.algorithme(drone, self.cells, self.connections)
                # THE HUB IS OCCUPIED SO THAT
                # THE DRONE MUST WAIT A TURN
                if not paths:
                    continue
                if paths[0].is_full() and paths[0] != drone.data.end_zone:
                    continue
                if paths[0] in drone.paths:
                    continue
                connection_name = join_name(drone.current_zone, paths[0])
                connection = self.connections[connection_name]
                # DRONE IS WAITING FOR THIS CONNECTION
                # TO BE AVAILABLE AGAIN, IN THE NEXT TURN
                place: list[Connection | Cell] | Any = paths[0]
                if paths[0].data.zone == 'restricted':
                    drone.current_conneciton =  connection
                    drone.restricted_next_zone = paths[0]
                    connection.increment_drones_by = 1
                    place = connection
                else:
                    drone.current_zone.increment_drones_by = -1
                    drone.current_zone = paths[0]
                    drone.paths.add(paths[0])
                    drone.current_zone.increment_drones_by = 1
                    if drone.current_zone == drone.data.end_zone:
                        self.drones.remove(drone)
                        self.temp_cells.append(drone)
                drone_turns.append(f"{drone.data.drone_id}-{place}")
            turn: str = " ".join(drone_turns)
            if turn:
                print(turn)
            turn_counter += 1
        print(turn_counter)
        return turn_counter
