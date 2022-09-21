import physics
from js import document, requestAnimationFrame
from pyodide import create_proxy
from objects import *
import pools
import events
from constants import CANVAS, CTX, UPDATE, RENDER, KEYDOWN, KEYUP
from agents import Human, RandomAI

keysdown = []
bullet_pool, asteroid_pool = pools.BulletPool(), pools.AsteroidPool()
ships = [Ship(player=1)]
player1 = Human(ships[0])
asteroid_pool.spawn_asteroid()

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
    if 'g' in keysdown:
        ships[0].create_miniships()
    UPDATE.trigger()

def act_agents():
    action = player1.act()
    ships[0].next_moves.extend(action)

def late_update():
    physics.check_objects(asteroid_pool.active_objects.copy(), bullet_pool.active_objects.copy(), ships.copy())

def game_loop(*args):
    act_agents()
    update()
    render()
    late_update()
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
 
