import time
from abc import ABC, abstractmethod
import constants
from js import console, document

def deboog(message):
    document.getElementById('output').innerHTML = message
    console.log(message)

class Event(ABC):
    def __init__(self):
        self.observers = []

    def suscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    
    def unsuscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    @abstractmethod
    def trigger(self):
        pass

class UpdateEvent(Event):
    def __init__(self):
        self.last_update = time.time()
        super(UpdateEvent, self).__init__()
    def trigger(self):
        delta_time = time.time() - self.last_update
        self.last_update = time.time()
        for observer in self.observers:
            observer.update(delta_time)
    
class RenderEvent(Event):
    def trigger(self):
        for observer in self.observers:
            observer.render()

class KeyDownEvent(Event):
    def trigger(self, key):
        for observer in self.observers:
            observer.on_key_down(key)

class KeyUpEvent(Event):
    def trigger(self, key):
        for observer in self.observers:
            observer.on_key_up(key)

class ObjectOutEvent(Event):
    def trigger(self, game_object):
        for observer in self.observers:
            observer.on_object_out(game_object)

class ShotEvent(Event):
    def trigger(self, player, pos, rot):
        for observer in self.observers:
            observer.on_bullet_shot(pos, rot, player)

class CollisionEvent(Event):
    def trigger(self, obj1, obj2):
        for observer in self.observers:
            observer.on_collision_enter(obj1, obj2)
            observer.on_collision_enter(obj2, obj1)

class AsteroidHitEvent(Event):
    def trigger(self, asteroid):
        for observer in self.observers:
            observer.on_asteroid_hit(asteroid)



