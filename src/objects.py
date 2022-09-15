import math
import constants
import events
from abc import ABC, abstractmethod
from constants import CTX, COLORS
from geometry import Vector2

class GameObject(ABC):
    def __init__(self, init_pos, points, dimension):
        constants.UPDATE.suscribe(self)
        constants.RENDER.suscribe(self)
        self.pos = init_pos
        self.points = points
        self.rotation = 0
        self.active = True
        self.dimension = dimension

    def translate(self):
        self.pos.x += self.speed * math.sin(self.rotation)
        self.pos.y -= self.speed * math.cos(self.rotation)
        self.keep_in_screen()

    def keep_in_screen(self):
        if self.pos.x > constants.CANVAS.width + self.dimension:
            self.pos.x = constants.CANVAS.width + self.dimension
        if self.pos.x < 0 +self.dimension * -1:
            self.pos.x = self.dimension * -1
        if self.pos.y > constants.CANVAS.height + self.dimension:
            self.pos.y = constants.CANVAS.height + self.dimension
        if self.pos.y < 0 + self.dimension * -1:
            self.pos.y = self.dimension * -1

    def prerender(self):
        CTX.save()
        CTX.translate(self.pos.x, self.pos.y)
        CTX.rotate(self.rotation)
        CTX.beginPath()
        return self.active
   
    def local_to_global(self, point):
        return self.pos + point

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
        super(Ship, self).__init__(init_pos, points, constants.RADIUS)

    def update(self):
        if self.active:
            self.accelerate()
            self.rotate()
            self.translate() 
            if constants.ACTIONS[4] in self.next_moves:
                self.shoot()
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
        if self.prerender():
            CTX.moveTo(self.points[0].x, self.points[0].y)
            for point in self.points[1:]:
                CTX.lineTo(point.x, point.y)
            CTX.fillStyle = COLORS['players'][self.player]['inner']
            CTX.fill()
            CTX.moveTo(self.points[0].x, self.points[0].y)
            CTX.lineTo(self.points[3].x, self.points[3].y)
            CTX.lineTo(self.points[2].x, self.points[2].y)
            CTX.fillStyle =  COLORS['players'][self.player]['outer']
            CTX.fill()  
        CTX.restore()

    def shoot(self):
        constants.SHOT.trigger(self.player, self.local_to_global(self.points[0]), self.rotation)

    

class Bullet(GameObject):
    def __init__(self):
        self.player = ""
        self.speed = constants.BULLET_SPEED
        width, points = self.init_points()
        # Voy a tener que iniciar la rotacion cuando los cree en el pool
        super(Bullet, self).__init__(Vector2(0,0), points, width)
    
    def activate(self, init_pos, rotation, player):
        self.pos = init_pos
        self.rotation = rotation
        self.player = player
        self.active = True

    def update(self):
        self.translate()
        pass
    
    def render(self):
        if self.prerender():
            CTX.moveTo(self.points[0].x, self.points[0].y)
            for point in self.points[1:]:
                CTX.lineTo(point.x, point.y)
            CTX.fillStyle = COLORS['bullet']
            CTX.fill()
        CTX.restore()

    def init_points(self):
        w = constants.RADIUS / 4
        h = constants.RADIUS
        return w, [Vector2(-w/2, -h/2), 
                Vector2(w/2, -h/2), 
                Vector2(w/2, h/2), 
                Vector2(-w/2, h/2)]

class Asteroid(GameObject):
    pass


    