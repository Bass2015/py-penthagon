from abc import ABC, abstractmethod
import random
import math

class GameObject(ABC):
    def __init__(self, update_ev, render_ev, ctx):
        update_ev.suscribe(self)
        render_ev.suscribe(self)
        self.ctx = ctx
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

class Circle(GameObject):
    def __init__(self, x, y, update_ev, render_ev, ctx):
       self.x = x
       self.y = y
       super(Circle, self).__init__(update_ev, render_ev, ctx)
    
    def update(self):
        self.x += random.randint(-3,3)
        self.y += random.randint(-3,3)
        super().update()

    def render(self):
        self.ctx.beginPath()
        self.ctx.arc(self.x, self.y, 10, 0, math.pi*2)
        self.ctx.fillStyle = 'red'
        self.ctx.fill()
        super().render()

class Rect(GameObject):
    def __init__(self, x, y, update_ev, render_ev, ctx):
       self.x = x
       self.y = y
       super(Rect, self).__init__(update_ev, render_ev, ctx)
    
    def update(self):
        self.x += random.randint(-1,1)
        self.y += random.randint(-1,1)
        super().update()

    def render(self):
        self.ctx.beginPath()
        self.ctx.rect(self.x, self.y, 20, 20)
        self.ctx.fillStyle = 'blue'
        self.ctx.fill()
        super().render()