from js import document, requestAnimationFrame
from pyodide import create_proxy
from events import RenderEvent
import events
from objects import Circle, Rect
import math

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
keysdown = []
update_ev = events.UpdateEvent()
render_ev = RenderEvent()


def on_key_down(*args):
    if args[0].key not in keysdown:
        keysdown.append(args[0].key) 
   
def on_key_up(*args):
    keysdown.remove(args[0].key)

def render(*args):
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    render_ev.trigger()

def update():
    pass

def game_loop(*args):
    update_ev.trigger()
    render()
    requestAnimationFrame(game_loop_proxy)
    
game_loop_proxy = create_proxy(game_loop)

def main():
    kdown_proxy = create_proxy(on_key_down)
    kup_proxy = create_proxy(on_key_up)
    document.addEventListener("keydown", kdown_proxy)
    document.addEventListener("keyup", kup_proxy)

    #Starts the game loop
    requestAnimationFrame(game_loop_proxy)

main()
 
