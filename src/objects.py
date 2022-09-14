from abc import ABC, abstractmethod
import random
import math
from constants import UPDATE, RENDER, CTX, ACTIONS

class GameObject(ABC):
    def __init__(self):
        UPDATE.suscribe(self)
        RENDER.suscribe(self)
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

class Circle(GameObject):
    def __init__(self, x, y):
       self.x = x
       self.y = y
       self.speed = 1
       self.next_moves = []
       super(Circle, self).__init__()
    
    def update(self):
        if ACTIONS[0] in self.next_moves:
            self.y -= self.speed
        if ACTIONS[1] in self.next_moves:
            self.y += self.speed 
        if ACTIONS[2] in self.next_moves:
            self.x -= self.speed
        if ACTIONS[3] in self.next_moves:
            self.x += self.speed
        # self.next_moves.clear()
        super().update()

    def render(self):
        CTX.beginPath()
        CTX.arc(self.x, self.y, 10, 0, math.pi*2)
        CTX.fillStyle = 'blue'
        if ACTIONS[4] in self.next_moves:
            CTX.fillStyle = 'red'
        CTX.fill()
        #SACAR ESTO DE AQUÍ Y PONERLO EN UPDATE
        self.next_moves.clear()
        super().render()


class Rect(GameObject):
    def __init__(self, x, y):
       self.x = x
       self.y = y
       super(Rect, self).__init__()
    
    def update(self):
        super().update()

    def render(self):
        CTX.beginPath()
        CTX.rect(self.x, self.y, 20, 20)
        CTX.fillStyle = 'blue'
        CTX.fill()
        super().render()