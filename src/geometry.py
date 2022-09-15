import math

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
   
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)