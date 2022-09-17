from hashlib import new
import math
import constants
import events
import time
import random
from abc import ABC, abstractmethod
from constants import AST_SPAWNING_LIMIT, CTX, COLORS
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
        
    def keep_in_screen(self):
        if self.pos.x > constants.CANVAS.width + self.dimension:
            self.pos.x = constants.CANVAS.width + self.dimension
        if self.pos.x < 0 +self.dimension * -1:
            self.pos.x = self.dimension * -1
        if self.pos.y > constants.CANVAS.height + self.dimension:
            self.pos.y = constants.CANVAS.height + self.dimension
        if self.pos.y < 0 + self.dimension * -1:
            self.pos.y = self.dimension * -1

    def check_boundaries(self):
        if (self.pos.x > constants.CANVAS.width + self.dimension or 
                self.pos.x < 0 +self.dimension * -1 or 
                self.pos.y > constants.CANVAS.height + self.dimension or 
                self.pos.y < 0 + self.dimension * -1):
            constants.OBJECTOUT.trigger(self)

    def prerender(self):
        CTX.save()
        CTX.translate(self.pos.x, self.pos.y)
        CTX.rotate(self.rotation)
        CTX.beginPath()
        return self.active
   
    def local_to_global(self, point):
        return self.pos + point.rotate(self.rotation)

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
        self.last_shot = 0
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
            self.keep_in_screen()
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
        if time.time() - self.last_shot > constants.SHOOTING_SPEED:
            constants.SHOT.trigger(self.player, self.local_to_global(self.points[0]), self.rotation)
            self.last_shot = time.time()

class Bullet(GameObject):
    def __init__(self):
        self.player = ""
        self.speed = constants.BULLET_SPEED
        width, points = self.init_points()
        # Voy a tener que iniciar la rotacion cuando los cree en el pool
        super(Bullet, self).__init__(Vector2(0,0), points, width)
    
    def __name__(self):
        return f"Bullet from player{self.player}"

    def activate(self, init_pos, rotation, player):
        self.pos = init_pos
        self.rotation = rotation
        self.player = player
        self.active = True

    def update(self):
        self.translate()
        self.check_boundaries()
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
        w = constants.RADIUS / 8
        h = constants.RADIUS
        return w, [Vector2(-w/2, -h/2), 
                Vector2(w/2, -h/2), 
                Vector2(w/2, h/2), 
                Vector2(-w/2, h/2)]

class Asteroid(GameObject):
    def __init__(self):
        self.speed = constants.AST_SPEED
        self.direction = Vector2.rand_unit()
        self.next_direction = Vector2.rand_unit()
        dim = constants.ASTEROID_RADIUS/8
        self.last_changed = 0
        self.change_time = 6
        super(Asteroid, self).__init__(Vector2(constants.CANVAS.width/2,
                                               constants.CANVAS.height/2),
                                       self.init_points(dim),
                                       dim)
    
    def __name__(self):
        return f"Asteroid"

    def activate(self):
        w, h = constants.CANVAS.width, constants.CANVAS.height
        X, Y = constants.AST_SPAWNING_LIMIT, constants.AST_SPAWNING_LIMIT
        W, H = w - 2 * X, h - 2 * Y
        coord = random.choice([(i % w,i/w ) for i in range(w*h) if (W > i * w - X > -1 < i / w - Y < H) < 1])
        self.pos = Vector2(coord[0], coord[1])
        self.activate = True
        self.direction = Vector2.rand_unit()
        self.next_direction = Vector2.rand_unit()


    def update(self):
        self.rotate()
        self.translate()

    def change_direction(self):
        elapsed_t = time.time() - self.last_changed
        new_direction = Vector2.lerp(self.direction, self.next_direction, elapsed_t/self.change_time)
        if elapsed_t > self.change_time:
            self.direction = self.next_direction
            self.next_direction = Vector2.rand_unit()
            self.last_changed = time.time()
        events.deboog(str(self.pos))
        return new_direction.normalized()

    def rotate(self):
        self.rotation += constants.AST_ROT_SPEED

    def translate(self):
        new_dir = self.change_direction()
        self.pos += self.speed * new_dir

    
    def render(self):
        if self.prerender():
            CTX.moveTo(self.points[0].x, self.points[0].y)
            for point in self.points[1:]:
                CTX.lineTo(point.x, point.y)
            CTX.fillStyle = COLORS['bullet']
            CTX.fill()
        CTX.restore()

    def init_points(self, radius):
        return [Vector2(radius * math.cos(math.radians(angle)), radius * math.sin(math.radians(angle))) for angle in range(0, 360, 45)]


    