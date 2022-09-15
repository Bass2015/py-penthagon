import math
from abc import ABC, abstractmethod
from pickle import NEWOBJ_EX
import constants
from constants import CTX
from geometry import Vector2
from js import document

class GameObject(ABC):
    def __init__(self, init_pos, points):
        constants.UPDATE.suscribe(self)
        constants.RENDER.suscribe(self)
        self.pos = init_pos
        self.points = points
        self.rotation = 0
        self.active = True

    def translate(self):
        self.pos.x += self.speed * math.sin(self.rotation)
        self.pos.y -= self.speed * math.cos(self.rotation)
        self.keep_in_screen()

    def keep_in_screen(self):
        if self.pos.x > constants.CANVAS.width + constants.RADIUS:
            self.pos.x = constants.CANVAS.width + constants.RADIUS
        if self.pos.x < 0 + constants.RADIUS * -1:
            self.pos.x = constants.RADIUS * -1
        if self.pos.y > constants.CANVAS.height + constants.RADIUS:
            self.pos.y = constants.CANVAS.height + constants.RADIUS
        if self.pos.y < 0 + constants.RADIUS * -1:
            self.pos.y = constants.RADIUS * -1

    def set_active(self, active):
        self.active = active

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

class Ship(GameObject):
    def __init__(self, init_pos, player):
        self.speed = 0
        self.max_speed = constants.SHIP_SPEED
        self.next_moves = []
        self.rot_speed = constants.ROT_SPEED
        self.acceleration = constants.SHIP_ACC
        self.player = player
        points = [Vector2(0, constants.RADIUS)]
        for angle in constants.ANGLES:
            points.append(Vector2(math.cos(math.radians(angle)) * constants.RADIUS, 
                           math.sin(math.radians(angle)) * constants.RADIUS))
        super(Ship, self).__init__(init_pos, points)

    def update(self):
        if self.active:
            self.accelerate()
            self.rotate()
            self.translate() 
            self.next_moves.clear()
            super().update()

    def accelerate(self):
        if constants.ACTIONS[0] in self.next_moves:
            self.speed = self.speed + self.acceleration if self.speed < self.max_speed else self.max_speed
        elif constants.ACTIONS[1] in self.next_moves:
            self.speed = self.speed - self.acceleration if self.speed > self.max_speed*-1 else self.max_speed*-1
        else:
            deceleration = math.copysign(constants.SHIP_DEC, self.speed)
            self.speed = self.speed - deceleration if not math.isclose(self.speed, 0, abs_tol=constants.SHIP_DEC) else self.speed * 0

    def rotate(self):
        if constants.ACTIONS[2] in self.next_moves:
            self.rotation -= self.rot_speed
        if constants.ACTIONS[3] in self.next_moves:
            self.rotation += self.rot_speed
    
    def render(self):
        if self.active:
            CTX.save()
            CTX.translate(self.pos.x, self.pos.y)
            CTX.rotate(self.rotation)
            CTX.beginPath()
            CTX.moveTo(self.points[0].x, self.points[0].y)
            for point in self.points[1:]:
                CTX.lineTo(point.x, point.y)
            CTX.fillStyle = 'lightcyan'
            CTX.fill()
            CTX.moveTo(self.points[0].x, self.points[0].y)
            CTX.lineTo(self.points[3].x, self.points[3].y)
            CTX.lineTo(self.points[2].x, self.points[2].y)
            CTX.fillStyle = 'coral'
            CTX.fill()  
            CTX.restore()
            super().render()

    def debug():
        document.getElementById("output").innerHTML = ""

class Bullet(GameObject):
    def __init__(self, init_pos, rotation, player):
        self.player = player
        self.rotation = rotation
        self.speed = constants.BULLET_SPEED
        self.pos = init_pos
    
    def update(self):
        self.translate()
        pass
    
    def render(self):
        CTX.save()
        CTX.translate


    