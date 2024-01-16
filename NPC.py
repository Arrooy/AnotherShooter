from Entity import ColisionEntity
from __init__ import Game
import random
import time
import math

class NPC(ColisionEntity):
    def __init__(self, id, x, y, hp, damage, attack_speed) -> None:
        super().__init__(id, x, y, 0, 0, max_speed=10)
        self.hp = hp
        self.maxHp = hp
        self.damage = damage
        
        self.attack_speed_ms = attack_speed
        self.last_attack_time = 0
        
        Game.npcs[self.id] = self
        
        if "npcs" not in Game.new_stuff:
             Game.new_stuff["npcs"] = {}
        
        Game.new_stuff["npcs"][self.id] = self
        
        
    def update(self):
        # Add logic here
        self.behave()
        super().update()
        # Check colision with other ColisionEntities.
        for i in Game.players:
            if self.check_colision(Game.players[i]):
                # Touched a player
                self.attack(Game.players[i])            
            
        if self.hp <= 0:
            self.toRemove = True 
    
    def behave(self):
        # Roam
        min_distance = None
        closest_player = None
        for i in Game.players:
            player = Game.players[i]
            distance = self.getDistance(player)
            if min_distance is None:
                min_distance = distance
                closest_player = player
            elif min_distance > distance:
                closest_player = player
                min_distance = distance
        
        if closest_player is not None:
            ## Found a player, follow it.
            self.vx = self.max_speed * (closest_player.x - self.x)/min_distance
            self.vy = self.max_speed * (closest_player.y - self.y)/min_distance
   
    
    
    def attack(self, player):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            player.hp -= 1
    
    def init_json(self):
        entity_json = super().toJson()
        player_json = {"maxHp":self.maxHp,"hp":self.hp}
        entity_json.update(player_json)
        return entity_json
    
    def update_json(self):
        entity_json = super().toJson()
        player_json = {"hp":self.hp}
        entity_json.update(player_json)
        return entity_json
