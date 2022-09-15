
from abc import ABC, abstractmethod
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
    def trigger(self):
        for observer in self.observers:
            observer.update()
    
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


