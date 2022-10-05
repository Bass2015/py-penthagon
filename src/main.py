from random import Random
import physics
from js import document, requestAnimationFrame
from pyodide import create_proxy
from objects import *
import pools
from constants import CANVAS, CTX, UPDATE, RENDER, KEYDOWN, KEYUP, GAME
from agents import Human, RandomAI
from ui_manager import UIManager

# modules for image processing



keysdown = []
bullet_pool, asteroid_pool = pools.BulletPool(), pools.AsteroidPool()
SHIPS = [Ship(player=1), Ship(player=2)]
PLAYERS = []
UIMANAGER = UIManager()

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
    CTX.beginPath()
    CTX.fillStyle = 'darkslategray'
    CTX.rect(0, 0, CANVAS.width, CANVAS.height)
    CTX.fill()
    RENDER.trigger()

def update():
    if 'g' in keysdown:
        pass
    UPDATE.trigger()

def act_agents():
    for i in range(2):
        if i < len(PLAYERS):
            action = PLAYERS[i].act()
            SHIPS[i].next_moves.extend(action)

def late_update():
    physics.check_objects(asteroid_pool.active_objects.copy(), bullet_pool.active_objects.copy(), SHIPS.copy())

def game_loop(*args):
    if GAME.frame_count % 2 == 0:
        start = time.time()
        act_agents()
        update()
        render()
        late_update()
        GAME.save_frame(CANVAS.toDataURL('image/png'))
        end = time.time()
    requestAnimationFrame(game_loop_proxy)
    GAME.frame_count += 1
    
game_loop_proxy = create_proxy(game_loop)

def main():
    kdown_proxy = create_proxy(on_key_down)
    kup_proxy = create_proxy(on_key_up)
    document.addEventListener("keydown", kdown_proxy)
    document.addEventListener("keyup", kup_proxy)

    #Starts the game loop

def human_vs_ai(*args):
    PLAYERS.clear()
    PLAYERS.extend([Human(SHIPS[0], player=1), 
                    RandomAI(SHIPS[1], player=2)])
    UIMANAGER.initialize(PLAYERS)
    constants.GAME_START.trigger()
    requestAnimationFrame(game_loop_proxy)
    

def human_vs_human(*args):
    PLAYERS.clear()
    PLAYERS.extend([Human(SHIPS[0], player=1), 
                    Human(SHIPS[1], player=2)])
    UIMANAGER.initialize(PLAYERS)
    requestAnimationFrame(game_loop_proxy)

main()
 
