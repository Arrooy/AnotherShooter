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

        self.hp = 10
        self.maxHp = 10
        self.toRemove = False
        Game.walls.append(self)

        if "walls" not in Game.new_stuff:
            Game.new_stuff["walls"] = {}

        Game.new_stuff["walls"][self.id] = self

    def update(self):
        if self.hp <= 0:
            self.hp = 0
            self.toRemove = True
            return

    def is_colliding_xy(self, x, y):
        return (
            x >= self.x
            and x <= self.x + self.w
            and y >= self.y
            and y <= self.y + self.h
        )

    def is_colliding(self, o):
        return self.is_colliding_xy(o.x, o.y)

    def init_json(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "color": self.color,
            "hp": self.hp,
            "maxHp": self.maxHp,
        }

    def update_json(self):
        return {"id": self.id, "hp": self.hp}
