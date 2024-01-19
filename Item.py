from Entity import ColisionEntity
import random

class Item(ColisionEntity):
    def __init__(self, name, carrier, active_function) -> None:
        # Compute x, y based on carrier. Dont overlap items.
        super().__init__(random.random(), carrier.x, carrier.y, 0, 0, 0, size=20)
        self.carrier = carrier
        self.name = name
        self.timer = 0
        self.droptime = 100
        self.active_function = active_function
        self.parent = None
        
    def update(self):
        self.x = self.carrier.x
        self.y = self.carrier.y
        self.timer+=1
        if self.timer > self.droptime:
            self.toRemove = True
    
    def pick_up(self, parent):
        self.parent = parent
        self.carrier = parent
        
    def activate(self):
        self.active_function(self.parent)
        self.parent.consume_item(self)
    
    def init_json(self):
        colision_entity_json = super().init_json()
        item_json = {"name":self.name}
        colision_entity_json.update(item_json)
        return colision_entity_json

class HealingPotion(Item):
    def __init__(self, carrier) -> None:
        super().__init__("Healing Potion", carrier, self.heal)
    
    def heal(self, parent):
        if parent is not None:
            parent.hp = parent.maxHp

class BigCashStack(Item):
    def __init__(self, carrier) -> None:
        super().__init__("Big cash stack", carrier, self.money)
    
    def money(self, parent):
        if parent is not None:
            parent.score += 5
            
