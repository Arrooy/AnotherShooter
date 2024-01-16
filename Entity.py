import math
from __init__ import Game

class Entity():
    def __init__(self, id, x, y, vx, vy, max_speed=20) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.max_speed = max_speed
        self.toRemove = False
    
    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    def getDistance(self, pt):
        return math.sqrt(math.pow(self.x - pt.x, 2) + math.pow(self.y - pt.y, 2))

    def toJson(self):
        return {"id":self.id, "x":self.x, "y":self.y, "vx":self.vx, "vy":self.vy}

class ColisionEntity(Entity):
    def __init__(self, id, x, y, vx, vy, max_speed=20) -> None:
        super().__init__(id, x, y, vx, vy, max_speed)
    
            
    def check_colision(self,objective):
        if self.getDistance(objective) < 32 and self.id != objective.id:
            # Repel the colision
            self.stop()
            objective.stop()
            return True
        return False
    
    def stop(self):
        self.x = self.x - self.vx
        self.y = self.y - self.vy
        self.vx = 0
        self.vy = 0