"""Config to lunch the application
"""


from utils.helper import generate_color

# SCREEN SETTINGS
WIDTH = 1280
HEIGHT = 600
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
