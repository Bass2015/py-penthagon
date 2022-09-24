from abc import ABC, abstractmethod
from pydoc import plain
import constants
from events import deboog
from constants import ACTIONS, KEYDOWN, KEYUP
from objects import Asteroid, Bullet
from js import document
import random
import time

class Agent(ABC):
    def __init__(self, ship, player=0):
        constants.SHIP_EXPLODED.suscribe(self)
        constants.COLLISION.suscribe(self)
        self.ship = ship
        self.lifes = 3
        self.score = 0
        self.player = player
    
    def get_action(self, action):
        if action == 0: # Forward
            return [ACTIONS[0]]
        if action == 1: # Backward
            return [ACTIONS[1]]
        if action == 2: # Left
            return [ACTIONS[2]]
        if action == 3: # Right
            return [ACTIONS[3]]
        if action == 4: # Forward Left
            return [ACTIONS[0], ACTIONS[2]]
        if action == 5: # Forward Right
            return [ACTIONS[0], ACTIONS[3]]
        if action == 6: # Backwards Left
            return [ACTIONS[1], ACTIONS[2]]
        if action == 7: # Backwards Right
            return [ACTIONS[1], ACTIONS[3]]
        if action == 8: # Forward Fire
            return [ACTIONS[0], ACTIONS[4]]
        if action == 9: # Forward Left Fire
            return [ACTIONS[0], ACTIONS[2], ACTIONS[4]]
        if action == 10: # Forward Right Fire
            return [ACTIONS[0], ACTIONS[3], ACTIONS[4]]
        if action == 11: # Backwards Fire
            return [ACTIONS[1], ACTIONS[4]]
        if action == 12: # Backwards Left Fire
            return [ACTIONS[1], ACTIONS[2], ACTIONS[4]]
        if action == 13: # Backwards Right Fire
            return [ACTIONS[1], ACTIONS[3], ACTIONS[4]]
        if action == 14: # Left Fire
            return [ACTIONS[2], ACTIONS[4]]
        if action == 15: # Left Fire
            return [ACTIONS[3], ACTIONS[4]]
        if action == 16: # Idle Fire
            return [ACTIONS[4]]
        if action == 17: # Idle
            return [ACTIONS[5]]

    def on_ship_exploded(self, ship):
        if ship.player == self.player:
            self.lifes -= 1
        else:
            self.score += 100
        constants.STATE_CHANGED.trigger()

    def on_collision_enter(self, obj1, obj2):
        if (isinstance(obj1, Asteroid) 
            and isinstance(obj2, Bullet) 
            and obj2.player == self.player):
            self.score += 10
            constants.STATE_CHANGED.trigger()

    @abstractmethod
    def act(*args):
        pass

class Human(Agent):
    def __init__(self, ship, player):
        KEYDOWN.suscribe(self)
        KEYUP.suscribe(self)
        self.keysdown = []
        super(Human, self).__init__(ship, player)
    
    def __str__(self):
        return "Agent Human"
   
    def act(self):  
        if 'w' in self.keysdown:
            if 'a' in self.keysdown:
                if ' ' in self.keysdown:
                    return self.get_action(9)
                return self.get_action(4)
            if 'd' in self.keysdown:
                if ' ' in self.keysdown:
                    return self.get_action(10)
                return self.get_action(5)
            if ' ' in self.keysdown:
                return self.get_action(8)
            return self.get_action(0)
        if 's' in self.keysdown:
            if 'a' in self.keysdown:
                if ' ' in self.keysdown:
                    return self.get_action(12)
                return self.get_action(6)
            if 'd' in self.keysdown:
                if ' ' in self.keysdown:
                    return self.get_action(13)
                return self.get_action(7)
            if ' ' in self.keysdown:
                return self.get_action(11)
            return self.get_action(1)
        if 'a' in self.keysdown:
            if ' ' in self.keysdown:
                return self.get_action(14)
            return self.get_action(2)
        if 'd' in self.keysdown:
            if ' ' in self.keysdown:
                return self.get_action(15)
            return self.get_action(3)
        if ' ' in self.keysdown:
            return self.get_action(16)
        return self.get_action(17)

    def on_key_down(self, key):
        if key not in self.keysdown:
              self.keysdown.append(key) 

    def on_key_up(self, key):
        if key in self.keysdown:
            self.keysdown.remove(key)

class RandomAI(Agent):
    def __init__(self, ship, player):
        self.last_change = time.time()
        self.change_time = 1.5
        self.current_move = 17
        super(RandomAI, self).__init__(ship, player)
    def act(self):
        if time.time() - self.last_change > self.change_time:
            self.current_move = random.randint(0,17)
            self.last_change = time.time()
        return self.get_action(self.current_move)
        