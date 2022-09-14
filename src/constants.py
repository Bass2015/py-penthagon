from js import document
import events

CANVAS = document.getElementById("canvas")
CTX = CANVAS.getContext("2d")
UPDATE = events.UpdateEvent()
RENDER = events.RenderEvent()
KEYDOWN = events.KeyDownEvent()
KEYUP = events.KeyUpEvent()
ACTIONS = {0: "FORWARD",
           1: "BACKWARD", 
           2: "LEFT", 
           3: "RIGHT",
           4: "FIRE",
           5: "IDLE"}
ANGLES = [162.0, 234.0, 306.0, 18.0]