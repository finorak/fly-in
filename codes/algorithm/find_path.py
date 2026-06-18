"""
IDEA FOR FINDING THE BEST NEXT CELL
USING A* FOR THE SHORTEST PATH.

ONCE THE PATH IS OCCUPIED BY A CELL,
WE VERIFY IF IT CAN STILL OCCUPY ANOTHER
DRONE, IF YES WE INCREMENT THE NUMBER OF CELL OCCUPIED
BY THAT CELL, IF NOT WE SUPPOSE THE CURRENT CELL CAN'T
BE REACHED. SO THAT THE DRONE WILL ATTEMPT TO FIND ANOTHER PATH
IF IT FIND, IF NOT IT WAIT.
"""


from queue import PriorityQueue
from typing import Any

import pygame
from src.cell import Cell
from src.connection import Connection
from src.drone import Drone


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
        conections: list[Connection]
        ) -> bool:
    """Finding the best next cell to go to
    Parameters:
        drone: the drone that need the best cell \
based on it's current cell
        cells: a dict containing all the cells.
        conections: the connections that the current cell \
has if it's utils to us
    Returns:
        boolean value that determin if we found \
the path or not
    """
    if drone.found_path:
        return True
    count = 0
    open_set: PriorityQueue = PriorityQueue()
    start_zone = drone.current_zone
    open_set.put((0, count, start_zone))
    end_zone = drone.data.end_zone
    came_from: dict[Cell, Cell] = {}
    g_score = {cells[pos]: float("inf") for pos in cells}
    g_score[drone.current_zone] = 0
    f_score = {cells[pos]: float("inf") for pos in cells}
    f_score[start_zone] = h(start_zone, end_zone)
    open_set_hash: set = {start_zone}
    start: bool = True
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
        current_zone: Cell = open_set.get()[2]
        open_set_hash.remove(current_zone)
        if current_zone == end_zone:
            drone.found_path = True
            drone.paths = list(came_from)
            return True
        for neighboor in current_zone.find_neighboor(conections):
            if start:
                came_from[neighboor] = start_zone
                start = False
            temp_g_score = g_score[current_zone] + 1
            if temp_g_score < g_score[neighboor]:
                came_from[neighboor] = current_zone
                g_score[neighboor] = temp_g_score
                f_score[neighboor] = temp_g_score + h(neighboor, end_zone)
                if neighboor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighboor], count, neighboor))
                    open_set_hash.add(neighboor)
    return False
