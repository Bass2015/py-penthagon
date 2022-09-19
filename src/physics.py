from geometry import Vector2
from objects import GameObject
import constants
import events

def check_objects(asteroids, bullets, *ships):
    collided = []
    for asteroid in asteroids:
        # for bullet in ships:
        if check_collision(asteroid, ships[0]):
            collided.extend([asteroid, ships[0]])
    if len(collided) > 0:
        constants.COLLISION.trigger(collided)
    collided.clear()

def check_collision(obj1:GameObject, obj2:GameObject):
    if obj1.dimension + obj2.dimension > Vector2.distance(obj1.pos, obj2.pos):
        return True
    
    
        

       