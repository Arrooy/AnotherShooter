import os
from flask import Flask, send_from_directory, render_template, current_app, request

from extensions import socketio
from werkzeug.local import LocalProxy

from flask_socketio import emit, Namespace
from random import random

import threading
import time
import math
import random

logger = LocalProxy(lambda: current_app.logger)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # Add favicon
    app.add_url_rule("/favicon.ico", view_func=lambda: send_from_directory(os.path.join(app.root_path, 'static'),
                                                                           'favicon.ico',
                                                                           mimetype='image/vnd.microsoft.icon'))

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template("index.html")
    
    socketio.on_namespace(Game('/game'))
    socketio.init_app(app)
    
    x = threading.Thread(target=Game.thread_function, args=(socketio,), daemon=True)
    x.start()
    
    return app


class Entity():
    def __init__(self, id, x, y, vx, vy) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.toRemove = False
    
    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    def getDistance(self, pt):
        return math.sqrt(math.pow(self.x - pt.x, 2) + math.pow(self.y - pt.y, 2))

    def toJson(self):
        return {"id":self.id, "x":self.x, "y":self.y, "vx":self.vx, "vy":self.vy}

class Weapon():
    def __init__(self, parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size) -> None:
        self.id = parent.id
        self.parent = parent
        self.max_bullet_speed = max_bullet_speed    
        self.range = range
        self.damage = damage
        self.bullet_size = bullet_size
        self.attack_speed_ms = attack_speed_ms
        self.last_attack_time = time.time_ns()

        
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            Bullet(self.parent, angle, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class Shotgun(Weapon):
    def __init__(self, parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
        
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            for i in range(-2,2):
                Bullet(self.parent, angle + i * 3, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class GranadeLauncher(Weapon):
    def __init__(self, parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
    
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            GranadeBullet(self.parent, angle, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class Player(Entity):
    def __init__(self, id, x, y) -> None:
        super().__init__(id, x, y, 0, 0)
        self.w = False
        self.d = False
        self.s = False
        self.a = False
        self.attackPressed = False
        self.mouseAngle = 0
        self.max_speed = 20
        self.hp = 10
        self.maxHp = 10
        self.score = 0
        self.current_weapon = 0
        self.weapons = [Weapon( self, max_bullet_speed=25, range=100, attack_speed_ms=150, damage=1, bullet_size=25),
                        Shotgun(self, max_bullet_speed=20, range=35,  attack_speed_ms=200, damage=0.1, bullet_size=10),
                        GranadeLauncher(self, max_bullet_speed=20, range=35,  attack_speed_ms=200, damage=0.1, bullet_size=10)]
        
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
        if self.attackPressed:
            self.shootBullet(self.mouseAngle)
            
        if self.hp <= 0:
            self.toRemove = True    
    
    def switch_weapon(self, weapon_number):
        if len(self.weapons) >= weapon_number:
            self.current_weapon = weapon_number - 1
        
    def shootBullet(self, angle):
        self.weapons[self.current_weapon].shootBullet(angle)
    
    def init_json(self):
        entity_json = super().toJson()
        player_json = {"maxHp":self.maxHp,"hp":self.hp, "score": self.score}
        entity_json.update(player_json)
        return entity_json
        
    def update_json(self):
        entity_json = super().toJson()
        player_json = {"hp":self.hp, "score": self.score}
        entity_json.update(player_json)
        return entity_json
        
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
            p = Game.players[i]
            if self.getDistance(p) < 32 and self.parentId != p.id:
                p.hp -= self.damage
                if p.hp <= 0:
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
        if self.toRemove:
            for i in range(0,360,10):
                Bullet(self, i, self.max_speed, 8, self.damage, self.size)
    
class Game(Namespace):
    """
        WebSocket Manager
    """
    players = {}
    bullets = {}
    new_stuff = {}
    
    def thread_function(sock):
        while True:
            while len(Game.players) == 0:
                time.sleep(0.5)
            try:
                
                remove = {"players":[], "bullets":[]}            
                for id in list(Game.players.keys()):
                    player = Game.players[id]
                    player.update()
                    
                    if player.toRemove:
                        remove["players"].append(id)
                        del Game.players[id]
                    
                for id in list(Game.bullets.keys()):
                    bullet = Game.bullets[id]
                    bullet.update()
                        
                    if bullet.toRemove:
                        remove["bullets"].append(id)
                        del Game.bullets[id]
                        
               
                if Game.new_stuff:
                    game_data = {
                        "bullets": [Game.new_stuff["bullets"][bullet].update_json() for bullet in Game.new_stuff["bullets"]]
                    }
                    socketio.emit("init", game_data, namespace="/game")
                    Game.new_stuff = {}
               
                if remove["players"] or remove["bullets"] :
                    socketio.emit("remove", remove, namespace="/game")
        
                game_data = {
                    "players": [Game.players[player].update_json() for player in Game.players],
                    "bullets": [Game.bullets[bullet].update_json() for bullet in Game.bullets]
                }
                socketio.emit("update", game_data, namespace="/game")
            except Exception as e: 
                print("Unable to send while loop.")
                print(e)
            time.sleep(0.04)


    def on_connect(self, data):
        Player(request.sid, 0,0)
        emit("player_connected", Game.players[request.sid].init_json(), broadcast=True, include_self=False)
        game_data = {
            "playerid":request.sid,
            "players": [Game.players[player].init_json() for player in Game.players],
            "bullets": [Game.bullets[bullet].update_json() for bullet in Game.bullets]
        }
        emit("init",game_data);

    def on_disconnect(self):
        emit("player_disconnected", request.sid, broadcast=True, include_self=False)
        if request.sid in Game.players:
            del Game.players[request.sid]
        print("A frontend disconnected.", request.sid)

    
    def on_keypress(self, data):
        
        if request.sid not in Game.players:
            return
        
        player = Game.players[request.sid]
        if(data["inputId"] == "w"):
            player.w = data["state"]
        if(data["inputId"] == "d"):
            player.d = data["state"]
        if(data["inputId"] == "s"):
            player.s = data["state"]
        if(data["inputId"] == "a"):
            player.a = data["state"]
        if data["inputId"] == "attack":
            player.attackPressed = data["state"]
        if data["inputId"] == "mouseAngle":
            player.mouseAngle = data["state"]
        if data["inputId"] == "switch_weapon":
            player.switch_weapon(data["state"])

