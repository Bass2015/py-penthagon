from js import document
import events
import math

CANVAS = document.getElementById("canvas")
CTX = CANVAS.getContext("2d")

# Game Events
UPDATE = events.UpdateEvent()
RENDER = events.RenderEvent()
KEYDOWN = events.KeyDownEvent()
KEYUP = events.KeyUpEvent()

# Actions
ACTIONS = {0: "FORWARD",
           1: "BACKWARD", 
           2: "LEFT", 
           3: "RIGHT",
           4: "FIRE",
           5: "IDLE"}

# Ship config
ANGLES = [162.0, 234.0, 306.0, 18.0]
RADIUS = -8 / math.cos(math.radians(54.0))
ROT_SPEED = math.pi/24
SHIP_SPEED = 5
SHIP_ACC = 0.5
SHIP_DEC = 0.05
BULLET_SPEED = 10
COLORS = {
    'player1': {
        'inner': 'lightcyan',
        'outer' : 'coral'
        },
    'bullet': 'black'}