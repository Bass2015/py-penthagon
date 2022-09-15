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
        CTX.beginPath()
        CTX.arc(self.pos.x, self.pos.y, 10, 0, math.pi*2)
        CTX.fillStyle = 'blue'
        if constants.ACTIONS[4] in self.next_moves:
            CTX.fillStyle = 'red'
        CTX.fill()
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
        self.accelerate()
        document.getElementById("output").innerHTML = f'{self.speed}'
        self.rotate()
        self.translate() 
        # self.next_moves.clear()
        super().update()

    def accelerate(self):
        if constants.ACTIONS[0] in self.next_moves:
            self.speed = self.speed + self.acceleration if self.speed < self.max_speed else self.max_speed
        elif constants.ACTIONS[1] in self.next_moves:
            self.speed = self.speed - self.acceleration if self.speed > self.max_speed*-1 else self.max_speed*-1
        else:
            deceleration = math.copysign(constants.SHIP_DEC, self.speed)
            self.speed = self.speed - deceleration if not math.isclose(self.speed, 0, abs_tol=constants.SHIP_DEC) else self.speed * 0

    def translate(self):
        newx =  self.pos.x + self.speed * math.sin(self.rotation)
        newy = self.pos.y - self.speed * math.cos(self.rotation)
        # self.keep_in_screen(newx, newy)
        if newx > constants.CANVAS.width + constants.RADIUS:
            newx = constants.CANVAS.width + constants.RADIUS
        if newx < 0 + constants.RADIUS * -1:
            newx = constants.RADIUS * -1
        if newy > constants.CANVAS.height + constants.RADIUS:
            newy = constants.CANVAS.height + constants.RADIUS
        if newy < 0 + constants.RADIUS * -1:
            newy = constants.RADIUS * -1
        self.pos.x = newx
        self.pos.y = newy

    def keep_in_screen(self, newx, newy):
        if newx > constants.CANVAS.width - constants.RADIUS:
            newx = constants.CANVAS.width - constants.RADIUS
        if newx < 0 + constants.RADIUS:
            newx = constants.RADIUS
        if newy > constants.CANVAS.height - constants.RADIUS:
            newy = constants.CANVAS.height - constants.RADIUS
        if newy < 0 + constants.RADIUS:
            # document.getElementById("output").innerHTML = 'OOOOUT!!!'
            newy = constants.RADIUS
        
        self.pos.x = newx
        self.pos.y = newy

    def rotate(self):
        if constants.ACTIONS[2] in self.next_moves:
            self.rotation -= self.rot_speed
        if constants.ACTIONS[3] in self.next_moves:
            self.rotation += self.rot_speed
    
    def render(self):
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
        if constants.ACTIONS[4] in self.next_moves:
            CTX.fillStyle = 'red'
        CTX.restore()
        #SACAR ESTO DE AQUÍ Y PONERLO EN UPDATE
        self.next_moves.clear()
        super().render()