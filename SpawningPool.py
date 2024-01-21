import time

from Item import HealingPotion, BigCashStack, SpeedPotion
from NPC import NPC
from random import random
from __init__ import Game

class SpawningPool():
    def __init__(self, x, y, max_units, list) -> None:
        self.x = x
        self.y = y
        self.max_units = max_units
        self.lastTime = time.time_ns()
        self.list = list
        self.time_ms = 1000
        
    def update(self):
        if len(self.list) >= self.max_units:
            return
        
        if time.time_ns() - self.lastTime >= 1_000_000 * self.time_ms:
            self.lastTime = time.time_ns()
            
            size = random() * 30 + 30
            
            x,y = Game.generate_empty_coords(self.x,self.y,size,size)
            npc = NPC(random(), x, y, int(size * 0.25), 1, attack_speed=500,size=size)
            magic_number = int(random() * 10);
            if magic_number <= 3: 
                npc.addItem(HealingPotion(npc))
            elif magic_number > 3 and magic_number <= 5:
                npc.addItem(BigCashStack(npc))
            
            npc.addItem(SpeedPotion(npc))