"""Config to lunch the application
"""


from typing import Any

from utils.helper import generate_color

#  SCREEN SETTINGS
WIN_SIZE = (1680, 920)  # AT SCHOOL
# WIN_SIZE = (1280, 580)  # AT HOME
TITLE = "Fly in"

# CELL SETTINGS
CELL_WIDTH = 80
CELL_HEIGHT = 10
CELL_WIDTH_GAP = 100
CELL_HEIGHT_GAP = 150

#  LINE
LINE_SIZE = 2

#  WHAT FORMAT WE ACCEPT IN THE CONFIG
#  VALUES AND KEYS
PATTERN = r'^\[[a-zA-Z_]\w*=[^=\s]+(?:\s+[a-zA-Z_]\w*=[^=\s]+)*\]$'

#  COLORS SETTINGS
BG_COLOR = generate_color("SandyBrown")
LINE_COLOR = generate_color("black")

#  ZONES WITH THEM DEFAULT VALUES
ZONES: dict[str, Any] = {
    'normal': {
        'color': 'blue',
        'cost': 1,
    },
    'restricted': {
        'color': 'purple',
        'cost': 2,
    },
    'priority': {
        'color': 'cyan',
        'cost': 1,
    },
    'blocked': {
        'color': 'red',
        'cost': float("inf"),
    }
}
