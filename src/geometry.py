import math

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
   
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def rotate(self, angle):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle) 
        return Vector2(x, y)
