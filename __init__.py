import os
from flask import Flask, send_from_directory, render_template, current_app, request

from extensions import socketio
from werkzeug.local import LocalProxy

from flask_socketio import emit, Namespace
from random import random

import threading
import time


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


class Game(Namespace):
    """
        WebSocket Manager
    """
    players = {}
    bullets = {}
    npcs = {}
    dropped_items = {}
    new_stuff = {}

    def update_list(list_id, dictionary, to_remove):
        for id in list(dictionary.keys()):
            item = dictionary[id]
            item.update()
            
            if item.toRemove:
                to_remove[list_id].append(id)
                del dictionary[id]
    
    def generate_empty_coords(spawn_x, spawn_y, area, size, iterations=0):
        if iterations >= 1:
            area = area + size
            
        x = spawn_x + random() * area - area/2 
        y = spawn_y + random() * area - area/2 
        
        for i in Game.npcs:
            npc = Game.npcs[i]
            if npc.getDistancexy(x,y) < npc.size/2+size/2:
                x,y = Game.generate_empty_coords(spawn_x, spawn_y, area, size, iterations+1)
        
        for i in Game.players:
            player = Game.players[i]
            if player.getDistancexy(x,y) < player.size/2+size/2:
                x,y = Game.generate_empty_coords(spawn_x, spawn_y, area, size, iterations+1)
        
        return x,y
        
    def thread_function(sock):
        from SpawningPool import SpawningPool
        spawning_pool = SpawningPool(500, 0, 50, Game.npcs)
        
        while True:
            while len(Game.players) == 0:
                time.sleep(0.5)
            #try:
            if True:
                             
                spawning_pool.update()
                
                to_remove = {"players":[], "bullets":[], "npcs":[], "dropped_items":[]}            
                
                # Update game and check for any entity that needs to be removed.
                Game.update_list("bullets", Game.bullets, to_remove)
                Game.update_list("players", Game.players, to_remove)
                Game.update_list("npcs", Game.npcs, to_remove)
                Game.update_list("dropped_items", Game.dropped_items, to_remove)
                
                # init data
                if Game.new_stuff:
                    game_data = {}
                    
                    if "bullets" in Game.new_stuff:
                        # Only add bullet if still exists.
                        game_data.update({"bullets": [Game.new_stuff["bullets"][bullet].update_json() for bullet in Game.new_stuff["bullets"] if not Game.new_stuff["bullets"][bullet].toRemove]})
                    
                    if "npcs" in Game.new_stuff:
                        game_data.update({"npcs": [Game.new_stuff["npcs"][npc].init_json() for npc in Game.new_stuff["npcs"]]})
                    
                    if "dropped_items" in Game.new_stuff:
                        game_data.update({"dropped_items": [Game.new_stuff["dropped_items"][item].init_json() for item in Game.new_stuff["dropped_items"]]})
                    
                    socketio.emit("init", game_data, namespace="/game")
                    Game.new_stuff = {}           
                     
                game_data = {
                    "players": [Game.players[player].update_json() for player in Game.players],
                    "bullets": [Game.bullets[bullet].update_json() for bullet in Game.bullets],
                    "npcs":    [Game.npcs[npc].update_json() for npc in Game.npcs],
                }
                socketio.emit("update", game_data, namespace="/game")
                
                # Remove data
                if to_remove["players"] or to_remove["bullets"] or to_remove["npcs"] or to_remove["dropped_items"]:
                    socketio.emit("remove", to_remove, namespace="/game")
                    
            """except Exception as e: 
                print("Unable to send while loop.")
                print(e)"""
            time.sleep(0.04)


    def on_start_game(self, name):
        
        from Player import Player
        x,y = Game.generate_empty_coords(-500,0,50,50)
        Player(request.sid, name, x, y, 50)
        emit("player_connected", Game.players[request.sid].init_json(), broadcast=True, include_self=False)
        game_data = {
            "playerid":request.sid,
            "players": [Game.players[player].init_json() for player in Game.players],
            "bullets": [Game.bullets[bullet].update_json() for bullet in Game.bullets],
            "npcs": [Game.npcs[npc].init_json() for npc in Game.npcs],
            "dropped_items":[Game.dropped_items[item].init_json() for item in Game.dropped_items],
        }
        emit("init",game_data)

    def on_disconnect(self):
        emit("player_disconnected", request.sid, broadcast=True, include_self=False)
        if request.sid in Game.players:
            del Game.players[request.sid]

    
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
        
        if(data["inputId"] == "use_item"):
            player.use_item(data["state"])
        
        if data["inputId"] == "attack":
            player.attackPressed = data["state"]
        if data["inputId"] == "mouseAngle":
            player.mouseAngle = data["state"]
        if data["inputId"] == "switch_weapon":
            player.switch_weapon(data["state"])

