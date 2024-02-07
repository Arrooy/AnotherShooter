from extensions import socketio
from __init__ import Game
from Weapon import Weapon, Shotgun, GranadeLauncher, Rocket, MachineGun, Sniper
from Entity import EntityWithItems
from math import sqrt 
from Item import BigCashStack


class Player(EntityWithItems):
    def __init__(self, id, name, x, y, size) -> None:
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
        self.money = 0

        self.current_weapon = 0
        self.weapons = [
            Weapon(self),
            Shotgun(self),
            GranadeLauncher(self),
            Rocket(self),
            MachineGun(self),
            Sniper(self),
        ]

        self.name = name

        Game.players[self.id] = self

    def update(self):
        if self.hp <= 0:
            self.hp = 0            
            # Convert money to items.
            for i in range(round(self.money / 5)):
                self.addItem(BigCashStack(self, 5))
            # Add more money as a reward.
            self.addItem(BigCashStack(self, 10))
            
            self.dropItems()
            self.toRemove = True
            return

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
        
        if self.vx != 0 and self.vy != 0:
            # Normalize vector
            self.vx = self.max_speed * self.vx / sqrt(pow(self.vx, 2) + pow(self.vy, 2))
            self.vy = self.max_speed * self.vy / sqrt(pow(self.vx, 2) + pow(self.vy, 2))
            
        
        super().update()
        
        # Check colision with walls.
        for wall in Game.walls:
            if wall.is_colliding(self):
                self.repel()
                break

        for i in list(self.items.keys()):
            item = self.items[i]
            if item.activated and item.has_effect:
                item.activate()

        # Check colision with other ColisionEntities.
        for i in Game.npcs:
            self.check_colision_stop(Game.npcs[i])

        # Check for colision with items
        for i in Game.dropped_items:
            item = Game.dropped_items[i]

            if self.check_colision(self.id, item):
                self.addItem(item)
                if item.manual_activation:
                    socketio.emit(
                        "item_grab", item.init_json(), namespace="/game", to=self.id
                    )
                else:
                    self.use_item(item.id)
                # Remove item from view
                item.toRemove = True

        if self.attackPressed:
            self.shootBullet(self.mouseAngle)

    def switch_weapon(self, weapon_number):
        if len(self.weapons) >= weapon_number:
            self.current_weapon = weapon_number - 1

    def shootBullet(self, angle):
        self.weapons[self.current_weapon].shootBullet(angle)

    def place_wall(self, blueprint):
        if self.money >= 10:
            self.money -= 10
            from Wall import Wall
            Wall(blueprint["x"],blueprint["y"],blueprint["w"],blueprint["h"])

    def init_json(self):
        entity_json = super().toJson()
        player_json = {
            "maxHp": self.maxHp,
            "size": self.size,
            "hp": self.hp,
            "score": self.score,
            "name": self.name,
        }
        entity_json.update(player_json)
        return entity_json

    def update_json(self):
        entity_json = super().toJson()
        player_json = {
            "hp": self.hp,
            "score": self.score,
            "money": self.money,
            "angle": self.mouseAngle,
        }
        entity_json.update(player_json)
        return entity_json
