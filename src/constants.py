from js import document
import events
import math

CANVAS = document.getElementById("canvas")
CTX = CANVAS.getContext("2d")
UI = document.getElementById("ui_canvas").getContext("2d")

GOLDEN_NUMBER = (1 + 5 ** 0.5) / 2

INIT_LIFES = 5
# Game Events
# meter todo esto en un diccionario
UPDATE = events.UpdateEvent()
RENDER = events.RenderEvent()
KEYDOWN = events.KeyDownEvent()
KEYUP = events.KeyUpEvent()
OBJECTOUT = events.ObjectOutEvent()
SHOT = events.ShotEvent()
COLLISION = events.CollisionEvent()
ASTEROID_HIT = events.AsteroidHitEvent()
SHIP_EXPLODED = events.ShipExplodedEvent()
STATE_CHANGED = events.StateChangedEvent()
GAME_ENDED = events.GameEndedEvent()
GAME_START = events.GameStartEvent()

# Actions
ACTIONS = {0: "FORWARD",
           1: "BACKWARD", 
           2: "LEFT", 
           3: "RIGHT",
           4: "FIRE",
           5: "IDLE"}

# Ship config
ANGLES = [162.0, 234.0, 306.0, 18.0]
RADIUS = -0.015 * max(CANVAS.width, CANVAS.height)
ROT_SPEED = 4.5
SHIP_SPEED = 350
SHIP_ACC = 30
SHIP_DEC = 10
SHOOTING_SPEED = 0.2
RESPAWN_TIME = 3
PHANTOM_TIME = 1.5
COLORS = {
    'players': {
        1: {
        'inner': 'rgb(255, 160, 122, {})',
        'outer': 'rgb(173, 216, 230, {})'
        }, 
        2: {
        'inner': 'rgb(34, 139, 34, {})',
        'outer': 'rgb(255, 215, 0, {})'
        }
    },
    'bullet': 'rgb(240, 248, 255)', 
    'asteroid': 'rgb(240, 248, 255)'}

# Miniship config
PENTAGON_SIDE = 2*RADIUS*math.sin(math.pi/5)
TALL_TRI_BASE =  PENTAGON_SIDE / (GOLDEN_NUMBER ** 2);
TALL_TRI_HEIGHT = PENTAGON_SIDE * math.sin(math.radians(36))
SHORT_TRI_HEIGHT = PENTAGON_SIDE * math.tan(math.radians(36)) / 2
DISTANCE_FROM_CENTER = RADIUS / 1.72
MINI_ANGLES = [90.0, 54.0, 18.0, 342.0, 306.0, 270.0, 234.0, 198.0, 162.0, 126.0]
# Bullet config
BULLET_SPEED = 1000

# Asteroid config
ASTEROID_RADIUS = .1 * max(CANVAS.width, CANVAS.height)
AST_SPEED = 20
AST_ROT_SPEED = math.pi/64
AST_SPAWNING_LIMIT = CANVAS.width * 0.1
AST_SPAWNING_CHANCE = 0.004
