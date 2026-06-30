"""Config to lunch the application
"""


from typing import Any

from utils.helper import generate_color

# SCREEN SETTINGS
WIN_SIZE = (1680, 920)
TITLE = "Fly in"

DRONE_LIMITS = 200

# CELL SETTINGS
CELL_WIDTH = 80
CELL_HEIGHT = 10
CELL_WIDTH_GAP = 100
CELL_HEIGHT_GAP = 150

# LINE
LINE_SIZE = 2

# WHAT FORMAT WE ACCEPT IN THE CONFIG
# VALUES AND KEYS
PATTERN = r'^\[[a-zA-Z_]\w*=[^=\s]+(?:\s+[a-zA-Z_]\w*=[^=\s]+)*\]$'

# COLORS SETTINGS
BG_COLOR = generate_color("SandyBrown")
LINE_COLOR = generate_color("black")

# ZONES WITH THEM DEFAULT VALUES
ZONES: dict[str, Any] = {
        'normal': {
            'color': '',
            'cost': 1,
            },
        'restricted': {
            'color': '',
            'cost': 2,
            },
        'priority': {
            'color': 'green',
            'cost': 1,
            },
        'blocked': {
            'color': 'red',
            'cost': float("inf"),
            }
        }
