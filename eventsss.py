
from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self):
        self.observers = []

    @abstractmethod
    def suscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    
    @abstractmethod
    def unsuscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    @abstractmethod
    def trigger(self):
        pass

class UpdatesEvent(Event):
    def trigger(self):
        for observer in self.observers:
            observer.update()
    def suscribe(self, observer):
        super().suscribe(observer)
    def unsuscribe(self, observer):
        super().unsuscribe(observer)

class RenderEvent(Event):
    def trigger(self):
        for observer in self.observers:
            observer.render()
    def suscribe(self, observer):
        super().suscribe(observer)
    def unsuscribe(self, observer):
        super().unsuscribe(observer)

