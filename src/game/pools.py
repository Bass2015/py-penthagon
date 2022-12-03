from distutils.spawn import spawn
import events
import constants
import random
from objects import Bullet, Asteroid, GameObject

class ObjectPool():
    def __init__(self):
        self.active_objects = []
        self.inactive_objects = []
        self.active = True
        constants.OBJECTOUT.suscribe(self)
        constants.GAME_ENDED.suscribe(self)
        constants.GAME_START.suscribe(self)

    def on_game_ended(self, looser):
        self.active_objects.clear()
        self.inactive_objects.clear()
        self.active = False

    def on_game_start(self):
        self.active = True
    
class BulletPool(ObjectPool):
    def __init__(self):
        constants.SHOT.suscribe(self)
        super(BulletPool, self).__init__()

    def get_bullet(self, init_pos, rotation, player):
        if not self.active: return
        if len(self.inactive_objects) == 0:
            bullet = Bullet()
        else:
            bullet = self.inactive_objects.pop()
        bullet.activate(init_pos, rotation, player)
        self.active_objects.append(bullet)
    
    def on_bullet_shot(self, pos, rot, player):
        self.get_bullet(pos, rot, player)
    
    def take_out(self, bullet:Bullet):
        if not isinstance(bullet, Bullet): return
        bullet.active = False
        self.inactive_objects.append(bullet)
        if bullet in self.active_objects:
            self.active_objects.remove(bullet)

    def on_object_out(self, game_object):
        if isinstance(game_object, Bullet):
            self.take_out(game_object)


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
        if isinstance(asteroid, Asteroid):
            asteroid.activate(size, pos)
            self.active_objects.append(asteroid)
    
    def update(self, delta_time):
        if not self.active: return
        if random.random() < constants.AST_SPAWNING_CHANCE:
            self.spawn_asteroid()

    def on_asteroid_hit(self, asteroid):
        self.spawn_asteroid(asteroid.dimension / 1.5, asteroid.pos)  
        self.spawn_asteroid(asteroid.dimension / 1.5, asteroid.pos)  
    
    def take_out(self, asteroid):
        if not isinstance(asteroid, Asteroid): return
        asteroid.active = False
        self.inactive_objects.append(asteroid)
        if asteroid in self.active_objects:
            self.active_objects.remove(asteroid)
    
    def on_object_out(self, game_object):
        if isinstance(game_object, Asteroid):
            self.take_out(game_object)

    