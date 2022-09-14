
from abc import ABC, abstractmethod

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


