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
from typing import Any

import pygame
from src.cell import Cell
from src.connection import Connection
from src.drone import Drone
from utils.helper import cell_lead_to_goal


def h(current_zone: Cell, end_zone: Cell) -> Any:
    """Getting the herestic of the function.
    We do so by calculating the cost of each
    turn
    Parameters:
        current_zone: the current zone to calculate
        end_zone: the end zone for our simulation
    Returns:
        the herestic value
    """
    return end_zone.data.turn_cost - current_zone.data.turn_cost


def algorithme(
        drone: Drone,
        cells: dict[tuple[int, int], Cell],
        connections: dict[str, Connection]
        ) -> bool:
    """Finding the best next cell to go to
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
    open_set.put((float("inf"), count, current_zone))
    end_zone = drone.data.end_zone
    came_from: dict[Cell, Cell] = {}
    g_score = {cells[pos]: float("inf") for pos in cells}
    g_score[drone.current_zone] = 0
    f_score = {cells[pos]: float("inf") for pos in cells}
    f_score[current_zone] = h(current_zone, end_zone)
    open_set_hash: set = {current_zone}
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
        current: Cell = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end_zone:
            drone.found_path = True
            drone.paths = list(came_from)
            return True
        for neighboor in current.find_neighboor(connections):
            # before going down that path
            # we first of all look if that path
            # can lead to 'end_hub' if not we don't go there
            print(current_zone, neighboor)
            if not cell_lead_to_goal(neighboor, end_zone):
                continue
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighboor]:
                came_from[neighboor] = current
                g_score[neighboor] = temp_g_score
                f_score[neighboor] = temp_g_score + h(neighboor, end_zone)
                if neighboor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighboor], count, neighboor))
                    open_set_hash.add(neighboor)
    return False


def solve(
        drones: list[Any],
        cells: dict[tuple[int, int], Cell],
        connections: dict[str, Connection]
        ) -> bool:
    """Solving the maze,
    Iterating over all the drones
    and trying to find the best solution
    Parameters:
        drones: a list of drones.
        cells: a list of cells.
        connections: list of connections
    """
    index: int = 0
    while drones:
        if algorithme(drones[index], cells, connections):
            print(*drones[index].paths, sep=" => ")
            drones.remove(drones[index])
        if len(drones) == 0:
            return True
        index = (index + 1) % len(drones)
    return True
