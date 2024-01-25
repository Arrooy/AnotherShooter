from Entity import ColisionEntity
import random
import time

class Item(ColisionEntity):
    def __init__(self, name, carrier, active_function, manual_activation=True, effect_time=0, deactivation_function=None, color="green") -> None:
        super().__init__(random.random(), carrier.x, carrier.y, 0, 0, 0, size=20)
        self.carrier = carrier
        self.name = name
        self.timer = 0
        self.droptime = 200
        self.active_function = active_function
        self.parent = None
        
        self.color = color
        
        self.manual_activation = manual_activation
        
        self.activated = False
        self.has_effect = effect_time != 0
        self.effect_time = effect_time
        self.effect_counter = 0
        self.deactivation_function = deactivation_function
        
    def update(self):
                    
        self.timer+=1
        if self.timer > self.droptime:
            print("removing item ", self.id)
            self.toRemove = True
    
    def pick_up(self, parent):
        self.parent = parent
        self.carrier = parent
        
    def activate(self):
        self.activated = True
        self.active_function(self.parent)
        if self.has_effect and time.time_ns() - self.effect_counter >= 1_000_000 * self.effect_time:
            self.deactivation_function(self.parent)
            self.parent.consume_item(self)
        elif not self.has_effect:
            self.parent.consume_item(self)
    
    def init_json(self):
        colision_entity_json = super().init_json()
        item_json = {"name":self.name, "color":self.color}
        colision_entity_json.update(item_json)
        return colision_entity_json

class HealingPotion(Item):
    def __init__(self, carrier) -> None:
        super().__init__("Healing Potion", carrier, self.heal, color="green")
    
    def heal(self, parent):
        if parent is not None:
            parent.hp = parent.maxHp

class BigCashStack(Item):
    def __init__(self, carrier, amount) -> None:
        super().__init__("Big cash stack", carrier, self.money, manual_activation=False, color="gold")
        self.amount = amount
        
    def money(self, parent):
        if parent is not None:
            parent.money += self.amount
            
class SpeedPotion(Item):
    def __init__(self, carrier) -> None:
        super().__init__("Speed potion", carrier, self.speed, 5000, self.de_activate, color="silver")
  
    def speed(self, parent):
        if parent is not None:
            parent.max_speed = parent.original_max_speed * 2
            
    def de_activate(self, parent):
        parent.max_speed = parent.original_max_speed