WIDTH = 900
HEIGHT = 650

BACKGROUND_COLOR = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

ZONE_COSTS = {
    "blocked": -1,
    "normal": 1,
    "priority": 1,
    "restricted": 2,
}

ZONE_COLOR = {
    "blocked": RED,
    "normal": BLUE,
    "start": GREEN,
    "end": GREEN,
    "junction": YELLOW,
    "priority": CYAN,
    "restricted": PURPLE,
}
