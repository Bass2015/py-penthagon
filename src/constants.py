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
OBJECTOUT = events.ObjectOutEvent()
SHOT = events.ShotEvent()
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
ROT_SPEED = math.pi/32
SHIP_SPEED = 4
SHIP_ACC = 0.3
SHIP_DEC = 0.1
SHOOTING_SPEED = 0.4
COLORS = {
    'players': {
        1: {
        'inner': 'coral',
        'outer': 'lightblue'
        }
    },
    'bullet': 'black'}


# Bullet config
BULLET_SPEED = 10

ASTEROID_RADIUS = RADIUS * 8
AST_SPEED = 0.5
AST_ROT_SPEED = math.pi/512