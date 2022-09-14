import math
from abc import ABC, abstractmethod
import constants
from geometry import Vector2

class GameObject(ABC):
    def __init__(self, init_pos, points):
        constants.UPDATE.suscribe(self)
        constants.RENDER.suscribe(self)
        self.pos = init_pos
        self.points = points
        self.rotation = 0
    
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
        points = []
        super(Circle, self).__init__(init_pos, points)
    
    def update(self):
        if constants.ACTIONS[0] in self.next_moves:
            self.pos.y -= self.speed
        if constants.ACTIONS[1] in self.next_moves:
            self.pos.y += self.speed 
        if constants.ACTIONS[2] in self.next_moves:
            self.pos.x -= self.speed
        if constants.ACTIONS[3] in self.next_moves:
            self.pos.x += self.speed
        # self.next_moves.clear()
        super().update()

    def render(self):
        constants.CTX.beginPath()
        constants.CTX.arc(self.pos.x, self.pos.y, 10, 0, math.pi*2)
        constants.CTX.fillStyle = 'blue'
        if constants.ACTIONS[4] in self.next_moves:
            constants.CTX.fillStyle = 'red'
        constants.CTX.fill()
        #SACAR ESTO DE AQUÍ Y PONERLO EN UPDATE
        self.next_moves.clear()
        super().render()

class Ship(GameObject):
    def __init__(self, init_pos):
        self.speed = constants.SHIP_SPEED
        self.next_moves = []
        self.rot_speed = constants.ROT_SPEED
        points = [Vector2(0, constants.RADIUS)]
        for angle in constants.ANGLES:
            points.append(Vector2(math.cos(math.radians(angle)) * constants.RADIUS, 
                           math.sin(math.radians(angle)) * constants.RADIUS))
        super(Ship, self).__init__(init_pos, points)

    def update(self):
        self.rotate()
        self.translate() 
        # self.next_moves.clear()
        super().update()

    def translate(self):
        if constants.ACTIONS[0] in self.next_moves:
            self.pos.x += self.speed * math.sin(self.rotation)
            self.pos.y -= self.speed * math.cos(self.rotation)
        if constants.ACTIONS[1] in self.next_moves:
            self.pos.x -= self.speed * math.sin(self.rotation)
            self.pos.y += self.speed * math.cos(self.rotation)

    def rotate(self):
        if constants.ACTIONS[2] in self.next_moves:
            self.rotation -= self.rot_speed
        if constants.ACTIONS[3] in self.next_moves:
            self.rotation += self.rot_speed
    
    def render(self):
        constants.CTX.save()
        constants.CTX.translate(self.pos.x, self.pos.y)
        constants.CTX.rotate(self.rotation)
        constants.CTX.beginPath()
        constants.CTX.moveTo(self.points[0].x, self.points[0].y)
        for point in self.points[1:]:
            constants.CTX.lineTo(point.x, point.y)
        constants.CTX.fillStyle = 'blue'
        if constants.ACTIONS[4] in self.next_moves:
            constants.CTX.fillStyle = 'red'
        constants.CTX.fill()
        constants.CTX.restore()
        #SACAR ESTO DE AQUÍ Y PONERLO EN UPDATE
        self.next_moves.clear()
        super().render()