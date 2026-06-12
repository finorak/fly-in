from utils.helper import generate_color

# SCREEN
WIDTH = 1280
HEIGHT = 720
TITLE = "Fly in"

# CELL
CELL_SIZE = 40

PATTERN = r'^\[[a-zA-Z_]\w*=[^=\s]+(?:\s+[a-zA-Z_]\w*=[^=\s]+)*\]$'

# COLORS
BG_COLOR = generate_color("SandyBrown")

# ZONES
ZONES = {
        'normal': {
            'color': ''
            },
        'blocked': {
            'color': ''
            },
        'restricted': {
            'color': ''
            },
        'priority': {
            'color': ''
            }
        }
