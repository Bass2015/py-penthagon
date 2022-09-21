from distutils.spawn import spawn
import events
import constants
import random
from objects import Bullet, Asteroid, GameObject

class ObjectPool():
    def __init__(self):
        self.active_objects = []
        self.inactive_objects = []
        constants.OBJECTOUT.suscribe(self)
    
    def take_out(self, game_object:GameObject):
        if game_object in self.active_objects:
            game_object.active = False
            object_from_active_pool = self.active_objects.index(game_object)
            if isinstance(object_from_active_pool, GameObject):
                self.inactive_objects.append(self.active_objects.pop(object_from_active_pool))
    
    def on_object_out(self, game_object):
        self.take_out(game_object)
    
class BulletPool(ObjectPool):
    def __init__(self):
        constants.SHOT.suscribe(self)
        super(BulletPool, self).__init__()

    def get_bullet(self, init_pos, rotation, player):
        if len(self.inactive_objects) == 0:
            bullet = Bullet()
        else:
            bullet = self.inactive_objects.pop()
        bullet.activate(init_pos, rotation, player)
        self.active_objects.append(bullet)
    
    def on_bullet_shot(self, pos, rot, player):
        self.get_bullet(pos, rot, player)

class AsteroidPool(ObjectPool):
    def __init__(self):
        constants.UPDATE.suscribe(self)
        constants.ASTEROID_HIT.suscribe(self)
        self.since_spawned = 0
        super(AsteroidPool, self).__init__()

    def spawn_asteroid(self, size=-1, pos=-1):
        if len(self.inactive_objects) == 0:
            asteroid = Asteroid()
        else:
            asteroid = self.inactive_objects.pop()
        asteroid.activate(size, pos)
        self.active_objects.append(asteroid)
    
    def update(self, delta_time):
        if random.random() < constants.AST_SPAWNING_CHANCE:
            self.spawn_asteroid()

    def on_asteroid_hit(self, asteroid):
        self.spawn_asteroid(asteroid.dimension / 1.5, asteroid.pos)  
        self.spawn_asteroid(asteroid.dimension / 1.5, asteroid.pos)  
    
        
    