from datetime import datetime
from js import document, requestAnimationFrame
from pyodide import create_proxy
import math

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
keysdown = []
circle = {
    'x': canvas.width/2,
    'y': canvas.height/2
}

def on_key_down(*args):
    if args[0].key not in keysdown:
        keysdown.append(args[0].key) 
    pyscript.write('output', f'Keys Pressed {keysdown}')

def on_key_up(*args):
    pyscript.write('output', f'Key Up {args[0].key}')
    keysdown.remove(args[0].key)

def render(*args):
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.beginPath()
    ctx.arc(circle['x'], circle['y'], 10, 0, math.pi*2)
    ctx.fillStyle = 'red'
    if 'b' in keysdown:
        ctx.fillStyle = 'blue'
    if 'g' in keysdown: 
        ctx.fillStyle = 'green'
    ctx.fill()

def update():
    if 'd' in keysdown:
        circle['x'] += 1
    if 'a' in keysdown:
        circle['x'] -= 1
    if 'w' in keysdown:
        circle['y'] -= 1
    if 's' in keysdown:
        circle['y'] += 1

def game_loop(*args):
    update()
    render()
    requestAnimationFrame(game_loop_proxy)
    
    
game_loop_proxy = create_proxy(game_loop)

def main():
    kdown_proxy = create_proxy(on_key_down)
    kup_proxy = create_proxy(on_key_up)
    document.addEventListener("keydown", kdown_proxy)
    document.addEventListener("keyup", kup_proxy)
    requestAnimationFrame(game_loop_proxy)

main()
 
