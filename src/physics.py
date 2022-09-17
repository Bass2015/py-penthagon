from geometry import Vector2
from objects import GameObject
import constants
import events

def check_objects(asteroids, bullets, *ships):
    # events.deboog("Checkin physics")
    collided = []
    for asteroid in asteroids:
        for bullet in bullets:
            if check_collision(asteroid, bullet):
                collided.extend([asteroid, bullet])
    constants.COLLISION.trigger(collided)

def check_collision(obj1:GameObject, obj2:GameObject):
    if obj1.dimension + obj2.dimension < Vector2.distance(obj1.pos, obj2.pos):
        events.deboog("COLLision")
        return True
    
        

       