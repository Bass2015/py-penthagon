from random import Random
from js import document, requestAnimationFrame, Blob, URL
from pyodide import create_proxy
import physics as physics
from objects import *
import pools
import events
from constants import CANVAS, CTX, UPDATE, RENDER, KEYDOWN, KEYUP, GAME, MATCH_ENDED
from agents import Human, RandomAI, QLearningAI
from ui_manager import UIManager
import time

keysdown = []
bullet_pool, asteroid_pool = pools.BulletPool(), pools.AsteroidPool()
SHIPS = [Ship(player=1), Ship(player=2)]
PLAYERS = []
UIMANAGER = UIManager()
frame = 0

class LoopObserver:
    def __init__(self):
        # No tiene que ser game ended, tiene que ser match ended
        MATCH_ENDED.suscribe(self)
        self.restart = False
    
    def on_match_ended(self):
        self.restart = True

LOOP_OBS = LoopObserver()

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
         PLAYERS[1].brain.update_net()
    UPDATE.trigger()

def act_agents(state):
    for i in range(2):
        if i < len(PLAYERS):
            action = PLAYERS[i].act(state)
            SHIPS[i].next_moves.extend(action)

def late_update():
    physics.check_objects(asteroid_pool.active_objects.copy(), bullet_pool.active_objects.copy(), SHIPS.copy())

def game_loop(*args):
    if GAME.frame_count % 2 == 0:
        # start = time.time()
        act_agents(GAME.state)
        # acting = time.time() - start
        # start = time.time()
        update()
        # upd = time.time() - start
        # start = time.time()
        render()
        # ren = time.time() - start
        # start = time.time()
        late_update()
        # late_up = time.time() - start
        # start = time.time()
        save_state()
        # show_times(acting, upd, ren, late_up, save_state)
    if LOOP_OBS.restart:
        on_match_end()
        LOOP_OBS.restart = False
    else: 
        requestAnimationFrame(game_loop_proxy)
    GAME.frame_count += 1

def show_times(acting, upd, ren, late_up, save_state):
    events.deboog(f'Act: {acting:.2f}</br>' + 
                      f'Update: {upd:.2f}</br>' +
                      f'Render: {ren:.2f}</br>' +
                      f'Collisions: {late_up:.2f}</br>' +
                      f'Saving state: {save_state:.2f}</br>' +
                      f'Total: {(acting + upd + ren + late_up + save_state):.2f}')
    
game_loop_proxy = create_proxy(game_loop)

def on_match_end():
    update()
    render()
    save_state()
    PLAYERS[1].on_match_ended(GAME.state)
    constants.GAME_START.trigger()
    render()
    save_state()
    requestAnimationFrame(game_loop_proxy)

match_end_proxy = create_proxy(on_match_end)

def main():
    kdown_proxy = create_proxy(on_key_down)
    kup_proxy = create_proxy(on_key_up)
    document.addEventListener("keydown", kdown_proxy)
    document.addEventListener("keyup", kup_proxy)

    #Starts the game loop

def human_vs_random(*args):
    GAME.cnn = False
    GAME.training = False
    start_game([Human(SHIPS[0], player=1), 
                    RandomAI(SHIPS[1], player=2)])

def human_vs_nn(*args):
    GAME.cnn = True
    GAME.training = False
    start_game([Human(SHIPS[0], player=1), 
                    QLearningAI(SHIPS[1], player=2)])

def human_vs_human(*args):
    GAME.cnn = False
    GAME.training = False
    start_game([Human(SHIPS[0], player=1), 
                    Human(SHIPS[1], player=2)])

def training(*args):
    GAME.cnn = True
    GAME.training = True
    start_game([Human(SHIPS[0], player=1),
                    QLearningAI(SHIPS[1], player=2, training=True)])

def start_game(players):
    PLAYERS.clear()
    PLAYERS.extend(players)
    UIMANAGER.initialize(PLAYERS)
    GAME.is_new_game = True
    constants.GAME_START.trigger()
    render()
    save_state()
    requestAnimationFrame(game_loop_proxy)

def save_state():
    GAME.save_state(CANVAS.toDataURL('image/png'))
    


main()
 
