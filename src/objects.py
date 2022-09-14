import math
from abc import ABC, abstractmethod
from constants import UPDATE, RENDER, CTX, ACTIONS, ANGLES
from game_config import RADIUS

class GameObject(ABC):
    def __init__(self, init_pos):
        UPDATE.suscribe(self)
        RENDER.suscribe(self)
        self.pos = init_pos
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

class Circle(GameObject):
    def __init__(self, init_pos):
       self.speed = 1
       self.next_moves = []
       super(Circle, self).__init__(init_pos)
    
    def update(self):
        if ACTIONS[0] in self.next_moves:
            self.pos.y -= self.speed
        if ACTIONS[1] in self.next_moves:
            self.pos.y += self.speed 
        if ACTIONS[2] in self.next_moves:
            self.pos.x -= self.speed
        if ACTIONS[3] in self.next_moves:
            self.pos.x += self.speed
        # self.next_moves.clear()
        super().update()

    def render(self):
        CTX.beginPath()
        CTX.arc(self.pos.x, self.pos.y, 10, 0, math.pi*2)
        CTX.fillStyle = 'blue'
        if ACTIONS[4] in self.next_moves:
            CTX.fillStyle = 'red'
        CTX.fill()
        #SACAR ESTO DE AQUÍ Y PONERLO EN UPDATE
        self.next_moves.clear()
        super().render()

class Ship(GameObject):
    def __init__(self, init_pos):
        self.speed = 1
        self.next_moves = []
        super(Circle, self).__init__(init_pos)

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
        CTX.save()
        CTX.translate(self.pos.x, self.pos.y)
        CTX.beginPath()
        CTX.arc(self.x, self.y, 10, 0, math.pi*2)
        CTX.fillStyle = 'blue'
        if ACTIONS[4] in self.next_moves:
            CTX.fillStyle = 'red'
        CTX.fill()
        #SACAR ESTO DE AQUÍ Y PONERLO EN UPDATE
        self.next_moves.clear()
        super().render()