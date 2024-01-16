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
    new_stuff = {}
    
    def thread_function(sock):
        
        from NPC import NPC
        while True:
            while len(Game.players) == 0:
                time.sleep(0.5)
            #try:
            if True:
                if random() < 0.01:
                    print("Creating Mob")
                    NPC(random(), 0, 0, 10, 1, 500)
                    
                remove = {"players":[], "bullets":[], "npcs":[]}            
                for id in list(Game.players.keys()):
                    player = Game.players[id]
                    player.update()
                    
                    if player.toRemove:
                        remove["players"].append(id)
                        del Game.players[id]
                
                for id in list(Game.npcs.keys()):
                    npc = Game.npcs[id]
                    npc.update()
                    
                    if npc.toRemove:
                        remove["npcs"].append(id)
                        del Game.npcs[id]
                
                for id in list(Game.bullets.keys()):
                    bullet = Game.bullets[id]
                    bullet.update()
                        
                    if bullet.toRemove:
                        remove["bullets"].append(id)
                        del Game.bullets[id]
                        
                if Game.new_stuff:
                    game_data = {}
                    
                    if "bullets" in Game.new_stuff:
                        game_data.update({"bullets": [Game.new_stuff["bullets"][bullet].update_json() for bullet in Game.new_stuff["bullets"]]})
                    
                    if "npcs" in Game.new_stuff:
                        game_data.update({"npcs": [Game.new_stuff["npcs"][npc].init_json() for npc in Game.new_stuff["npcs"]]})
                    
                    socketio.emit("init", game_data, namespace="/game")
                    Game.new_stuff = {}
               
                if remove["players"] or remove["bullets"] or remove["npcs"] :
                    socketio.emit("remove", remove, namespace="/game")
        
                game_data = {
                    "players": [Game.players[player].update_json() for player in Game.players],
                    "bullets": [Game.bullets[bullet].update_json() for bullet in Game.bullets],
                    "npcs":    [Game.npcs[npc].update_json() for npc in Game.npcs],
                }
                socketio.emit("update", game_data, namespace="/game")
            """except Exception as e: 
                print("Unable to send while loop.")
                print(e)"""
            time.sleep(0.04)


    def on_connect(self, data):
        from Player import Player
        Player(request.sid, 0,0)
        emit("player_connected", Game.players[request.sid].init_json(), broadcast=True, include_self=False)
        game_data = {
            "playerid":request.sid,
            "players": [Game.players[player].init_json() for player in Game.players],
            "bullets": [Game.bullets[bullet].update_json() for bullet in Game.bullets],
            "npcs": [Game.npcs[npc].init_json() for npc in Game.npcs],
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
        if data["inputId"] == "attack":
            player.attackPressed = data["state"]
        if data["inputId"] == "mouseAngle":
            player.mouseAngle = data["state"]
        if data["inputId"] == "switch_weapon":
            player.switch_weapon(data["state"])

