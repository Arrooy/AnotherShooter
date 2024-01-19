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
    def __init__(self, id, x, y, vx, vy, max_speed=20, size=32) -> None:
        super().__init__(id, x, y, vx, vy, max_speed)
        self.size = size
    
    def check_colision(self, myId, objective):
        return self.getDistance(objective) < (self.size/2+objective.size/2) and myId != objective.id
             
    def check_colision_repel(self,objective):
        if self.check_colision(self.id, objective):
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
        
    def init_json(self):
        entity_json = super().toJson()
        colision_entity_json = {"size":self.size}
        entity_json.update(colision_entity_json)
        return entity_json
        

class EntityWithItems(ColisionEntity):
    def __init__(self, id, x, y, vx, vy, max_speed=20, size=32) -> None:
        super().__init__(id, x, y, vx, vy, max_speed, size)
        self.items = {}
        
    def addItem(self, item):
        # Todo: agrupar per tipo de item.
        self.items[item.id] = item
        item.pick_up(self)
    
    def consume_item(self, item):
        del self.items[item.id]
    
    def dropItems(self):
        for i in self.items:
            item = self.items[i]
            Game.dropped_items[item.id] = item
            
            if "dropped_items" not in Game.new_stuff:
                Game.new_stuff["dropped_items"] = {}
            
            Game.new_stuff["dropped_items"][item] = item
        
    def use_item(self, id):
        print("Activating item", id)
        print("My Items are", self.items)
        #if id in self.items:
        self.items[id].activate()