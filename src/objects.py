import math
from abc import ABC, abstractmethod
import constants
from geometry import Vector2
from js import document

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
        self.speed = 0
        self.max_speed = constants.SHIP_SPEED
        self.next_moves = []
        self.rot_speed = constants.ROT_SPEED
        self.acceleration = constants.SHIP_ACC
        points = [Vector2(0, constants.RADIUS)]
        for angle in constants.ANGLES:
            points.append(Vector2(math.cos(math.radians(angle)) * constants.RADIUS, 
                           math.sin(math.radians(angle)) * constants.RADIUS))
        super(Ship, self).__init__(init_pos, points)

    def update(self):
        if constants.ACTIONS[0] in self.next_moves:
            self.speed = self.speed + self.acceleration if self.speed < self.max_speed else self.max_speed
        elif constants.ACTIONS[1] in self.next_moves:
            self.speed = self.speed - self.acceleration if self.speed > self.max_speed*-1 else self.max_speed*-1
        else:
            deceleration = constants.SHIP_DEC * -1 if self.speed < 0 else constants.SHIP_DEC
            self.speed = self.speed - deceleration if not math.isclose(self.speed, 0, rel_tol=0.1) else 0
        document.getElementById("output").innerHTML = self.speed
        self.rotate()
        self.translate() 
        # self.next_moves.clear()
        super().update()

    def translate(self):
        self.pos.x += self.speed * math.sin(self.rotation)
        self.pos.y -= self.speed * math.cos(self.rotation)

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