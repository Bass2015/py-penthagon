from js import document, requestAnimationFrame
from pyodide import create_proxy
from objects import Bullet, Ship
import pools
from constants import CANVAS, CTX, UPDATE, RENDER, KEYDOWN, KEYUP
from agents import Human, RandomAI
from geometry import Vector2

keysdown = []
bullet_pool, asteroid_pool = pools.BulletPool(), pools.AsteroidPool()
ship1 = Ship(Vector2(CANVAS.width/2, CANVAS.height/2), player=1)
# bullet = Bullet(Vector2(CANVAS.width/2, CANVAS.height/2), player=1)
player1 = Human(ship1)

def on_key_down(*args):
    if args[0].key not in keysdown:
        keysdown.append(args[0].key) 
    KEYDOWN.trigger(args[0].key)
   
def on_key_up(*args):
    if args[0].key in keysdown:
        keysdown.remove(args[0].key)
    KEYUP.trigger(args[0].key)

def render(*args):
    CTX.clearRect(0, 0, CANVAS.width, CANVAS.height)
    RENDER.trigger()

def update():
    UPDATE.trigger()

def act_agents():
    action = player1.act()
    ship1.next_moves.extend(action)

def game_loop(*args):
    act_agents()
    update()
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
 
