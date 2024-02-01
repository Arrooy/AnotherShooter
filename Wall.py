from __init__ import Game
from random import random
class Wall:
    def __init__(self, x, y, w, h, color="slategrey") -> None:
        self.id = random()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        Game.walls.append(self)
        
    def is_colliding(self, o):
        return (
            o.x >= self.x
            and o.x <= self.x + self.w
            and o.y >= self.y
            and o.y <= self.y + self.h
        )
        
    def init_json(self):
        return {"id": self.id, "x":self.x, "y":self.y, "w":self.w, "h":self.h, "color": self.color}