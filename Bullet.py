from __init__ import Game
from Entity import Entity

import math
import random


class Bullet(Entity):
    def __init__(self, parent, angle, max_speed, range, damage, bullet_size) -> None:
        vx_ = math.cos(angle/180.0*math.pi) * max_speed
        vy_ = math.sin(angle/180.0*math.pi) * max_speed
        super().__init__(random.random(), parent.x, parent.y, vx_, vy_)
        self.timer = 0
        self.range = range
        self.parentId = parent.id
        self.damage = damage
        self.size = bullet_size
        self.max_speed = max_speed
        
        Game.bullets[self.id] = self
        
        if "bullets" not in Game.new_stuff:
             Game.new_stuff["bullets"] = {}
        
        Game.new_stuff["bullets"][self.id] = self
    
    def update(self):
        self.timer+=1
        if self.timer > self.range:
            self.toRemove = True
            
        super().update()
        
        for i in Game.players:
            self.check_colision(Game.players[i])
        
        for i in Game.npcs:
            self.check_colision(Game.npcs[i])
        
    def check_colision(self, objective):
            
        if objective.hp > 0 and self.getDistance(objective) < (self.size/2 + objective.size/2) and self.parentId != objective.id:
            objective.hp -= self.damage
            if objective.hp <= 0:
                shooter = Game.players[self.parentId]
                if shooter:
                    shooter.score += 1
                
            self.toRemove = True
    
    
    def update_json(self):
        entity_json = super().toJson()
        bullet_json = {"size":self.size}
        entity_json.update(bullet_json)
        return entity_json
    
class GranadeBullet(Bullet):
    def __init__(self, parent, angle, max_speed, range, damage, bullet_size) -> None:
        super().__init__(parent, angle, max_speed, range, damage, bullet_size)
        self.parent = parent
        
    def update(self):
        super().update()
        # Activate granade
        if self.toRemove and self.timer > self.range:
            for i in range(0,360,10):
                b = Bullet(self.parent, i, self.max_speed, 8, self.damage / 10, self.size)
                b.x = self.x
                b.y = self.y
    