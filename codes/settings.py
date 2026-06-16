"""Config to lunch the application
"""


from utils.helper import generate_color

# SCREEN SETTINGS
WIDTH = 720
HEIGHT = 360
TITLE = "Fly in"

# CELL SETTINGS
CELL_WIDTH = 80
CELL_HEIGHT = 10
CELL_WIDTH_GAP = 100
CELL_HEIGHT_GAP = 150

# LINE
LINE_SIZE = (5, 5)

# WHAT FORMAT WE ACCEPT IN THE CONFIG
# VALUES AND KEYS
PATTERN = r'^\[[a-zA-Z_]\w*=[^=\s]+(?:\s+[a-zA-Z_]\w*=[^=\s]+)*\]$'

# COLORS SETTINGS
BG_COLOR = generate_color("SandyBrown")
LINE_COLOR = generate_color("black")

# ZONES WITH THEM DEFAULT VALUES
ZONES = {
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
            'cost': -1,
            }
        }
