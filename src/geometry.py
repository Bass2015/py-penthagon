import math
import numpy as np

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
   
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        """ Returns Hadamard product if two vectors, 
        or multiplies vector values by number if int or float """
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        raise ValueError(f'Multiplication with type {type(other)} not supported')
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return (f'Vector[{self.x}, {self.y}]')

    def __str__(self):
        return self.__repr__()
    
    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def normalized(self):
        """ Returns a normalized unit vector """        
        norm = self.norm()
        return  Vector2(self.x/norm, self.y / norm)

    def rotate(self, angle):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle) 
        return Vector2(x, y)

    def lerp(v1, v2, t):
        if (not isinstance(v1, Vector2) or
             not isinstance(v2, Vector2) or
             not isinstance(t, float)):
            raise ValueError(f'Interpolation needs two vectors and a float')
        return v1 * t + v2 * (1-t)

    def rand_unit():
        points = np.random.normal(0, 1, 2)
        return Vector2(points[0], points[1]).normalized()
