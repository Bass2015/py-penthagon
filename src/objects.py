import math, constants, time, random, geometry, easings, events
from pyodide import create_proxy
from js import setInterval
from abc import ABC, abstractmethod
from constants import AST_SPAWNING_LIMIT, CTX, COLORS
from geometry import Vector2

class GameObject(ABC):
    def __init__(self, init_pos, points, dimension):
        constants.UPDATE.suscribe(self)
        constants.RENDER.suscribe(self)
        constants.COLLISION.suscribe(self)
        constants.GAME_ENDED.suscribe(self)
        constants.GAME_START.suscribe(self)
        self.pos = init_pos
        self.points = points
        self.rotation = 0
        self.active = True
        self.dimension = dimension
        self.collided = False
       
    def __str__(self):
        return self.__name__()

    def translate(self, delta_time):
        self.pos.x += self.speed * math.sin(self.rotation) * delta_time
        self.pos.y -= self.speed * math.cos(self.rotation) * delta_time
        
    def keep_in_screen(self):
        if self.pos.x > constants.CANVAS.width - self.dimension:
            self.pos.x = constants.CANVAS.width - self.dimension
        if self.pos.x < 0 +self.dimension:
            self.pos.x = self.dimension 
        if self.pos.y > constants.CANVAS.height - self.dimension:
            self.pos.y = constants.CANVAS.height - self.dimension
        if self.pos.y < 0 + self.dimension:
            self.pos.y = self.dimension

    def check_boundaries(self):
        if not self.active:
            return
        if (self.pos.x > constants.CANVAS.width + self.dimension or 
                self.pos.x < 0 + self.dimension * -1 or 
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

    def on_collision_enter(self, me, other):
        self.collided = True

    def on_game_ended(self, loser):
        self.active = False

    @abstractmethod
    def update(self, delta_time):
        pass

    def on_game_start(self):
        pass

    def render(self):
        if self.prerender():
            CTX.moveTo(self.points[0].x, self.points[0].y)
            for point in self.points[1:]:
                CTX.lineTo(point.x, point.y)
            CTX.fillStyle = self.color
            CTX.fill()
        CTX.restore()

class Ship(GameObject):
    def __init__(self, player):
        self.speed = 0
        self.max_speed = constants.SHIP_SPEED
        self.next_moves = []
        self.rot_speed = constants.ROT_SPEED
        self.acceleration = constants.SHIP_ACC
        self.player = player
        self.last_shot = 0
        self.miniships = self.create_miniships()
        self.phantom = True
        self.activation_time = time.time()
        self.respawning = False
        points = [Vector2(0, constants.RADIUS)]
        for angle in constants.ANGLES:
            points.append(Vector2(math.cos(math.radians(angle)) * constants.RADIUS, 
                           math.sin(math.radians(angle)) * constants.RADIUS))
        super(Ship, self).__init__(Vector2((constants.CANVAS.width/3) * self.player, constants.CANVAS.height/2),points, constants.RADIUS * -1)
    
    def __name__(self):
            return f"Ship from player {self.player}"

    def on_game_ended(self, looser):
        self.respawning = False
        self.phantom = False
        self.next_moves.clear()
        super().on_game_ended(looser)
    
    def on_game_start(self):
        self.next_moves.clear()
        self.active = True
        self.respawning = False
        self.phantom = True
        self.collided = False
        self.rotation = 0
        self.pos = Vector2((constants.CANVAS.width/3) * self.player, constants.CANVAS.height/2)

    def create_miniships(self):
        miniships = []
        for i in range(0, 10):
            miniship = Miniship(i, self.player)
            miniship.active = False
            miniships.append(miniship)
        return miniships
        
    def update(self, delta_time):
        if self.active:
            self.accelerate()
            self.rotate(delta_time)
            self.translate(delta_time) 
            self.keep_in_screen()
            if constants.ACTIONS[4] in self.next_moves:
                self.shoot()
            self.next_moves.clear()
            if self.phantom:
                self.deactivate_phantom()
        elif self.respawning:
            self.wait_for_respawn()

    def deactivate_phantom(self):
        if time.time() - self.activation_time > constants.PHANTOM_TIME:
            self.phantom = False

    def wait_for_respawn(self):
        if time.time() - self.hit_time > constants.RESPAWN_TIME:
            self.respawn()

    def respawn(self):
        self.active = True
        self.respawning = False
        self.phantom = True
        self.next_moves.clear()
        self.speed = 0
        self.activation_time = time.time()

    def accelerate(self):
        if constants.ACTIONS[0] in self.next_moves:
            self.speed = self.speed + self.acceleration if self.speed < self.max_speed else self.max_speed
        elif constants.ACTIONS[1] in self.next_moves:
            self.speed = self.speed - self.acceleration if self.speed > self.max_speed*-1 else self.max_speed*-1
        else:
            deceleration = math.copysign(constants.SHIP_DEC, self.speed)
            self.speed = self.speed - deceleration if not math.isclose(self.speed, 0, abs_tol=constants.SHIP_DEC) else self.speed * 0

    def rotate(self, delta_time):
        if constants.ACTIONS[2] in self.next_moves:
            self.rotation -= self.rot_speed * delta_time
        if constants.ACTIONS[3] in self.next_moves:
            self.rotation += self.rot_speed * delta_time
    
    def render(self):
        if self.prerender():
            CTX.moveTo(self.points[0].x, self.points[0].y)
            for point in self.points[1:]:
                CTX.lineTo(point.x, point.y)
            opacity = 0.4 if self.phantom else 1
            CTX.fillStyle = COLORS['players'][self.player]['inner'].format(opacity)
            CTX.fill()
            CTX.moveTo(self.points[0].x, self.points[0].y)
            CTX.lineTo(self.points[3].x, self.points[3].y)
            CTX.lineTo(self.points[2].x, self.points[2].y)
            CTX.fillStyle =  COLORS['players'][self.player]['outer'].format(opacity)
            CTX.fill()  
        CTX.restore()

    def shoot(self):
        if time.time() - self.last_shot > constants.SHOOTING_SPEED:
            constants.SHOT.trigger(self.player, self.local_to_global(self.points[0]), self.rotation)
            self.last_shot = time.time()

    def on_collision_enter(self, me, other):
        if self.am_I_hit(me, other):
            self.active = False
            self.respawning = True  
            self.hit_time = time.time() 
            constants.SHIP_EXPLODED.trigger(self)

    def trigger_explosion(self):
        for i in range(len(self.miniships)):
            self.miniships[i].activate(self.pos)
            self.miniships[i].init_explosion()

    def am_I_hit(self, me, other):
        one, two = False, False
        prompt= ""
        if self.active:
            prompt += "I'm active"
            if not self.phantom:
                prompt += ", i'm not phantom"
                if self == me:
                    prompt += ", it's me"
                    one = True
        if (isinstance(other, Asteroid) or
            (isinstance(other, Bullet) and
                other.player != self.player)):
            two = True
        # if self.player == 1: events.deboog(prompt)
        return one and two


class Bullet(GameObject):
    def __init__(self):
        self.player = ""
        self.speed = constants.BULLET_SPEED
        width, points = self.init_points()
        self.color = constants.COLORS['bullet']

        # Voy a tener que iniciar la rotacion cuando los cree en el pool
        super(Bullet, self).__init__(Vector2(0,0), points, width * -1)
    
    def __name__(self):
        return f"Bullet from player{self.player}"

    def activate(self, init_pos, rotation, player):
        self.pos = init_pos
        self.rotation = rotation
        self.player = player
        self.active = True
        self.collided = False

    def update(self, delta_time):
        self.translate(delta_time)
        self.check_boundaries()
        pass
    
    def init_points(self):
        w = constants.RADIUS / 8
        h = constants.RADIUS
        return w, [Vector2(-w/2, -h/2), 
                Vector2(w/2, -h/2), 
                Vector2(w/2, h/2), 
                Vector2(-w/2, h/2)]

    def on_collision_enter(self, me, other):
        if (self == me and
            isinstance(other, Asteroid)): #or
            #(isinstance(other, Ship) and other.player != self.player))):
            constants.OBJECTOUT.trigger(self)
            super().on_collision_enter(me, other)

class Asteroid(GameObject):
    def __init__(self):
        self.speed = constants.AST_SPEED
        self.direction = Vector2.rand_unit()
        self.next_direction = Vector2.rand_unit()
        dim = constants.ASTEROID_RADIUS
        self.last_changed = time.time()
        self.change_time = 6
        self.color = constants.COLORS['asteroid']
        super(Asteroid, self).__init__(Vector2(constants.CANVAS.width/2,
                                               constants.CANVAS.height/2),
                                       self.init_points(dim),
                                       dim)
    
    def __name__(self):
        return f"Asteroid"

    def activate(self, size, pos):
        if size == -1:
            divisions = round(random.gauss(2,0.6))
            if divisions == 4:
                constants.OBJECTOUT.trigger(self)
                return
            if divisions != 0:
                self.dimension = constants.ASTEROID_RADIUS / (divisions * 1.5) 
        else:
            self.dimension = size
        self.points = self.init_points(self.dimension)
        if pos == -1:
            x, y = geometry.random_point_within_limit(AST_SPAWNING_LIMIT)
            self.pos = Vector2(x, y)
        else:
            self.pos = pos
        self.active = True
        self.direction = Vector2.rand_unit()
        self.next_direction = Vector2.rand_unit()
        self.collided = False
        
    def update(self, delta_time):
        if self.active:
            self.rotate(delta_time)
            self.translate(delta_time)
            self.check_boundaries()

    def change_direction(self):
        elapsed_t = time.time() - self.last_changed
        new_direction = Vector2.lerp(self.direction, self.next_direction, elapsed_t/self.change_time)
        if elapsed_t > self.change_time:
            self.direction = self.next_direction
            self.next_direction = Vector2.rand_unit()
            self.last_changed = time.time()
        return new_direction.normalized()

    def rotate(self, delta_time):
        self.rotation += constants.AST_ROT_SPEED * delta_time

    def translate(self, delta_time):
        new_dir = self.change_direction()
        fixed_speed = self.speed * delta_time
        self.pos += fixed_speed * new_dir 
    
    def on_collision_enter(self, me, other):
        if (self.not_hit(me, other)):
            return
        constants.OBJECTOUT.trigger(self)
        super().on_collision_enter(me, other)
        if self.dimension > constants.ASTEROID_RADIUS / (1.5*3):
            constants.ASTEROID_HIT.trigger(self)

    def not_hit(self, me, other):
        return (self.collided or
            self != me or
            isinstance(other, Asteroid) or
            (isinstance(other, Ship) and
            other.phantom))

    def init_points(self, radius):
        return [Vector2(radius * math.cos(math.radians(angle)), radius * math.sin(math.radians(angle))) for angle in range(0, 360, 45)]

class Miniship(GameObject):
    def __init__(self, index, player):
        constants.SHIP_EXPLODED.suscribe(self)
        self.speed = constants.AST_SPEED
        self.exploded = False
        self.identity = index
        self.player = player
        if index % 2 == 0:
            self.points = Miniship.tall_triangle_points()
            self.color = constants.COLORS['players'][self.player]['inner'].format(1)
            self.rotation = math.pi - math.pi*index/5 
            self.direction = Vector2(0,1).rotate(self.rotation)
        else:
            self.points = Miniship.short_triangle_points()
            self.color = constants.COLORS['players'][self.player]['outer'].format(1)
            self.rotation = -math.pi*index/5
            self.direction = Vector2(0,1).rotate(self.rotation - math.pi)
        super(Miniship, self).__init__(Vector2(constants.CANVAS.width/2, constants.CANVAS.height/2),
                                        self.points,
                                        constants.TALL_TRI_BASE)
    
    def activate(self, init_pos):
        self.active = True
        self.pos = Vector2(constants.DISTANCE_FROM_CENTER * math.cos(math.radians(constants.MINI_ANGLES[self.identity])),
                           constants.DISTANCE_FROM_CENTER * math.sin(math.radians(constants.MINI_ANGLES[self.identity]))) + init_pos

    def on_ship_exploded(self, ship):
        if not isinstance(ship, Ship):
            raise ValueError("Only accept type Ship")
        if ship.player == self.player:
            self.activate(ship.pos)
            self.explosion_moment = time.time()
            self.explosion_pos = self.pos
            self.elapsed_time = 0
            self.exploded = True

    def explosion(self, delta_time):
        final_pos = (self.explosion_pos + self.direction*80)
        explosion_time = 2
        if self.elapsed_time/explosion_time < 1:
            self.pos = Vector2.lerp(self.explosion_pos,
                                    final_pos,
                                    easings.ease_out_expo(self.elapsed_time/explosion_time))
            self.elapsed_time += delta_time
            self.rotation += 0.2 - easings.ease_out_circ(0.2)
            return
        self.active = False
        self.exploded = False
    
    def tall_triangle_points():
        return [Vector2(0, -constants.TALL_TRI_HEIGHT / 2),
                Vector2( -constants.TALL_TRI_BASE / 2, constants.TALL_TRI_HEIGHT / 2),
                Vector2( constants.TALL_TRI_BASE / 2, constants.TALL_TRI_HEIGHT / 2)]

    def short_triangle_points():
        return [Vector2(0, -constants.SHORT_TRI_HEIGHT / 2),
                Vector2( -constants.PENTAGON_SIDE / 2, constants.SHORT_TRI_HEIGHT / 2),
                Vector2( constants.PENTAGON_SIDE / 2, constants.SHORT_TRI_HEIGHT / 2)]
    
    def update(self, delta_time):
        if self.exploded:
            self.explosion(delta_time)        # self.translate(delta_time)
        
    





  