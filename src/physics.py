from geometry import Vector2
from objects import GameObject
import constants

def check_objects(asteroids, bullets, ships):
    for asteroid in asteroids:
        for ship in ships:
            check_collision(asteroid, ship)
        for bullet in bullets:
                check_collision(bullet, ship)
                check_collision(asteroid, bullet)
   
def check_collision(obj1:GameObject, obj2:GameObject):
    if (not obj1.active or not obj2.active):
        return
    if obj1.dimension + obj2.dimension > Vector2.distance(obj1.pos, obj2.pos):
        constants.COLLISION.trigger(obj1, obj2)

    
    
        

       