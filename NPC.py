from Entity import EntityWithItems
from __init__ import Game
from random import random
import time
import math

class NPC(EntityWithItems):
    def __init__(self, id, x, y, hp, damage, attack_speed, size) -> None:
        super().__init__(id, x, y, 0, 0, max_speed=10, size=size)
        self.hp = hp
        self.maxHp = hp
        self.damage = damage
        
        self.attack_speed_ms = attack_speed
        self.last_attack_time = 0
        
        self.state = 0
        self.last_state = 0
        self.last_roam = 0
        
        self.heading = 0
        
        Game.npcs[self.id] = self
        
        if "npcs" not in Game.new_stuff:
             Game.new_stuff["npcs"] = {}
        
        Game.new_stuff["npcs"][self.id] = self
        
        
    def update(self):
        if self.hp <= 0:
            self.hp = 0
            self.dropItems()
            self.toRemove = True 
            return
        
        self.heading = math.atan2(self.vy, self.vx) / math.pi * 180.0
        
        closest_player, distance = self.find_closest_player()
        
        # Add logic here
        self.behave(closest_player, distance)
        super().update()
        
        for wall in Game.walls:
            if wall.is_colliding(self):
                self.repel()
                break
        
        # Check colision with other ColisionEntities.
        if closest_player is not None and self.check_colision_stop(closest_player):
            # Touched a player
            self.attack(closest_player)
        
        # Repel otrher npcs
        for i in Game.npcs:
            self.check_colision_repel(Game.npcs[i])
        
       
    
    def behave(self, closest_player, distance):
        if closest_player is not None and distance < 500:
            self.state = 4
            
        if self.state == 0:
            # Stop
            self.vx = 0
            self.vy = 0
            if time.time_ns() - self.last_roam > 1_000_000 * (random() * 1000 + 500):
                self.last_roam = time.time_ns()
                self.state = 1
                
        elif self.state == 1:
            self.vx = random() * self.max_speed - self.max_speed/2
            self.vy = random() * self.max_speed - self.max_speed/2
            self.last_roam = time.time_ns()
            self.state = 3
        elif self.state == 3:
            # Roam
            if time.time_ns() - self.last_roam > 1_000_000 * (random() * 1000 + 500):
                self.last_roam = time.time_ns()
                self.state = 0
            
        elif self.state == 4:
            # Follow
            isFollowing = self.follow(closest_player, distance)
            if not isFollowing:
                self.state = 0
        
    def follow(self, closest_player, min_distance):
        if closest_player is not None and min_distance != 0 and min_distance < 500:
            ## Found a player, follow it.
            self.vx = self.max_speed * (closest_player.x - self.x)/min_distance
            self.vy = self.max_speed * (closest_player.y - self.y)/min_distance
            return True
        else:
            return False
    
    def find_closest_player(self):
        # Find closest player
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
        
        return closest_player, min_distance
    
    
    def attack(self, player):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            player.hp -= self.damage
    
    def init_json(self):
        entity_json = super().toJson()
        player_json = {"maxHp":self.maxHp, "size": self.size, "hp":self.hp}
        entity_json.update(player_json)
        return entity_json
    
    def update_json(self):
        entity_json = super().toJson()
        player_json = {"hp":self.hp, "heading" : self.heading}
        entity_json.update(player_json)
        return entity_json
