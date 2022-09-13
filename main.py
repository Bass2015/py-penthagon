from datetime import datetime
from js import document, Math, setInterval
from pyodide import create_proxy
import math

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
keysdown = []

def on_key_down(*args):
    if args[0].key not in keysdown:
        keysdown.append(args[0].key) 
    pyscript.write('output', f'Keys Pressed {keysdown}')

def on_key_up(*args):
    pyscript.write('output', f'Key Up {args[0].key}')
    keysdown.remove(args[0].key)

def render(*args):
    ctx.beginPath()
    ctx.arc(canvas.width/2, canvas.height/2, 10, 0, math.pi*2)
    ctx.fillStyle = 'red'
    if 'b' in keysdown:
        ctx.fillStyle = 'blue'
    if 'g' in keysdown: 
        ctx.fillStyle = 'green'
    ctx.fill()
   
def main():
    kdown_proxy = create_proxy(on_key_down)
    kup_proxy = create_proxy(on_key_up)
    render_proxy = create_proxy(render)
    document.addEventListener("keydown", kdown_proxy)
    document.addEventListener("keyup", kup_proxy)
    


main()
 
