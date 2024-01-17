from __init__ import Game
from Weapon import Weapon, Shotgun, GranadeLauncher, Rocket, MachineGun
from Entity import ColisionEntity
    
class Player(ColisionEntity):
    def __init__(self, id, x, y, size) -> None:
        super().__init__(id, x, y, 0, 0, size=size)
        self.w = False
        self.d = False
        self.s = False
        self.a = False
        self.attackPressed = False
        self.mouseAngle = 0
        self.hp = 10
        self.maxHp = 10
        self.score = 0
        self.current_weapon = 0
        self.weapons = [Weapon(self), Shotgun(self), GranadeLauncher(self), Rocket(self), MachineGun(self)]
        
        Game.players[self.id] = self
        
    def update(self):
        if self.w:
            self.vy = -self.max_speed
        elif self.s:
            self.vy = self.max_speed
        else: 
            self.vy = 0
            
        if self.d:
            self.vx = self.max_speed
        elif self.a:
            self.vx = -self.max_speed
        else:
            self.vx = 0
        
        super().update()
        
        # Check colision with other ColisionEntities.
        for i in Game.npcs:
            self.check_colision(Game.npcs[i])
            
        if self.attackPressed:
            self.shootBullet(self.mouseAngle)
            
        if self.hp <= 0:
            self.hp = 0
            self.toRemove = True    
    
    def switch_weapon(self, weapon_number):
        if len(self.weapons) >= weapon_number:
            self.current_weapon = weapon_number - 1
        
    def shootBullet(self, angle):
        self.weapons[self.current_weapon].shootBullet(angle)
    
    def init_json(self):
        entity_json = super().toJson()
        player_json = {"maxHp":self.maxHp, "size":self.size, "hp":self.hp, "score": self.score}
        entity_json.update(player_json)
        return entity_json
        
    def update_json(self):
        entity_json = super().toJson()
        player_json = {"hp":self.hp, "score": self.score}
        entity_json.update(player_json)
        return entity_json
