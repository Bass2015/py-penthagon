import constants
from objects import Bullet, Asteroid, GameObject


class ObjectPool():
    def __init__(self):
        self.active_objects = []
        self.inactive_objects = []
        constants.OBJECTOUT.suscribe(self)
    
    def take_out(self, game_object:GameObject):
        if game_object in self.active_objects:
            game_object.active = False
            self.inactive_objects.append(self.active_objects.remove(game_object))
    
class BulletPool(ObjectPool):
    def __init__(self):
        constants.SHOT.suscribe(self)
        super(BulletPool, self).__init__()

    def get_bullet(self, init_pos, rotation, player):
        if len(self.inactive_objects) == 0:
            bullet = Bullet()
        else:
            bullet = self.inactive_objects().pop()
        bullet.activate(init_pos, rotation, player)
        self.active_objects.append(bullet)
    
    def on_bullet_shot(self, pos, rot, player):
        self.get_bullet(pos, rot, player)

class AsteroidPool(ObjectPool):
    pass
    
    
        
    