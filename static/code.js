var htmlCanvas = document.getElementById("canvas");
var ctx = htmlCanvas.getContext("2d");

var htmlCanvasUi = document.getElementById("canvasui");
var ctxUi = htmlCanvasUi.getContext("2d");

let leftPress = false;
let rightPress = false;
let upPress = false;
let downPress = false;
let socket;
let players = {};
let bullets = {};
let npcs = {};
let dropped_items = {};
let mysocketid;

let world_x = 0;
let world_y = 0;

const background_image = new Image();
background_image.src = "static/background1.png";

const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

class Entity {
    constructor(initPack) {
        this.id = initPack.id;
        this.x = initPack.x;
        this.y = initPack.y;
        this.size = initPack.size;
        this.dx = this.x;
        this.dy = this.y;
        this.vx = 0;
        this.vy = 0;
    }


    update() {
        this.vx = (this.dx - this.x) / 2
        this.vy = (this.dy - this.y) / 2

        this.x += this.vx;
        this.y += this.vy;
    }
}

class ColisionEntity extends Entity {
    constructor(initPack) {
        super(initPack);
        this.hp = initPack.hp;
        this.maxHp = initPack.maxHp;
    }

    drawHpBar(x, y) {
        // HP bar
        let hpmw = 5 * this.maxHp
        let hph = 4
        let hpWidth = hpmw * this.hp / this.maxHp;
        let hpx = x - hpmw / 2;
        let hpy = y - this.size - hph - 10;

        ctx.strokeStyle = "black"
        ctx.fillStyle = "red";
        ctx.fillRect(hpx, hpy, hpmw, hph);
        ctx.strokeRect(hpx, hpy, hpmw + 1, hph + 1)
        ctx.fillStyle = "green";
        ctx.fillRect(hpx, hpy, hpWidth, hph)
    }
}

class Player extends ColisionEntity {
    constructor(initPack) {
        super(initPack);
        this.angle = 0;
        this.score = 0;
        this.money = 0;
        this.name = initPack.name;
        players[this.id] = this;
    }

    update() {
        super.update()
    }

    draw() {

        let x, y;
        if (!isMobile) {
            x = this.x - players[mysocketid].x + htmlCanvas.width / 2;
            y = this.y - players[mysocketid].y + htmlCanvas.height / 2;
        } else {
            x = world_x + this.x;
            y = world_y + this.y;
        }

        super.drawHpBar(x, y);

        ctx.fillStyle = "black";
        ctx.font = "16px serif";
        ctx.textAlign = "center";
        ctx.fillText(this.name, x, y - 40);

        this.drawRotatedPlayer(x, y);
    }

    drawRotatedPlayer(x, y) {
        let width = this.size;
        let height = this.size;
        x = x - width / 2;
        y = y - height / 2;
        // first save the untranslated/unrotated context
        ctx.save();

        ctx.beginPath();
        // move the rotation point to the center of the rect
        ctx.translate(x + width / 2, y + height / 2);
        // rotate the rect
        ctx.rotate(this.angle * Math.PI / 180);

        // draw the rect on the transformed context
        // Note: after transforming [0,0] is visually [x,y]
        //       so the rect needs to be offset accordingly when drawn

        // Player
        let nx = -width / 2;
        let ny = -height / 2;
        ctx.fillStyle = "blue";
        ctx.fillRect(nx, ny, width, height);
        ctx.strokeRect(nx, ny, width, height);

        ctx.fillStyle = "blue";
        ctx.fillRect(nx + width - 1, ny + height / 2 - 10, 20, 20)
        ctx.strokeRect(nx + width - 1, ny + height / 2 - 10, 20, 20);


        // restore the context to its untranslated/unrotated state
        ctx.restore();

    }
}

class NPC extends ColisionEntity {
    constructor(initPack) {
        super(initPack);
        npcs[this.id] = this;
    }

    update() {
        super.update()
    }

    draw() {
        let x, y;
        if (!isMobile) {
            x = this.x - players[mysocketid].x + htmlCanvas.width / 2;
            y = this.y - players[mysocketid].y + htmlCanvas.height / 2;
        } else {
            x = world_x + this.x;
            y = world_y + this.y;
        }
        super.drawHpBar(x, y);

        ctx.fillStyle = "brown";
        ctx.fillRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
        ctx.strokeRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
    }
}

class Bullet extends Entity {
    constructor(initPack) {
        super(initPack);
        bullets[this.id] = this;
    }

    update() {
        super.update()
    }

    draw() {

        let x, y;
        if (!isMobile) {
            x = this.x - players[mysocketid].x + htmlCanvas.width / 2;
            y = this.y - players[mysocketid].y + htmlCanvas.height / 2;
        } else {
            x = world_x + this.x;
            y = world_y + this.y;
        }

        ctx.fillStyle = "red";
        ctx.fillRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
        ctx.strokeRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
    }
}

class Item extends Entity {
    constructor(initPack) {
        super(initPack);
        this.color = initPack.color;
        dropped_items[this.id] = this;
    }

    draw() {
        let x, y;
        if (!isMobile) {
            x = this.x - players[mysocketid].x + htmlCanvas.width / 2;
            y = this.y - players[mysocketid].y + htmlCanvas.height / 2;
        } else {
            x = world_x + this.x;
            y = world_y + this.y;
        }

        ctx.fillStyle = this.color;
        ctx.fillRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
        ctx.strokeRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
    }
}
class Game {

    static drawMap() {
        const game_width = 2000
        const game_height = 2000
        let x, y;
        if (!isMobile) {
            x = -game_width / 2 - players[mysocketid].x + htmlCanvas.width / 2;
            y = -game_height / 2 - players[mysocketid].y + htmlCanvas.height / 2;
        } else {
            x = world_x - game_width / 2 + htmlCanvas.width / 2;
            y = world_y - game_height / 2 + htmlCanvas.height / 2;
        }
        const tile_width = 499;
        const tile_height = 499;
        for (let i = 0; i < Math.ceil(game_width / tile_width) - 1; i++) {
            for (let h = 0; h < Math.ceil(game_height / tile_height - 1); h++) {
                ctx.drawImage(background_image, x + i * tile_width, y + h * tile_height);
            }
        }

        ctx.strokeStyle = "slategrey";
        ctx.strokeRect(x, y, 2000, 2000);
    }

    static drawEntities() {

        for (const bullet in bullets) {
            bullets[bullet].draw();
        }

        for (const player in players) {
            players[player].draw();
        }

        for (const npc in npcs) {
            npcs[npc].draw();
        }

        for (const item in dropped_items) {
            dropped_items[item].draw();
        }
    }
}

class UI {

    static draw() {

        UIStats.drawScore();
    }
}

class UIStats {

    constructor() {
        this.lastScore = -1;
        this.lastMoney = -1;
    }

    static drawScore() {
        let score = players[mysocketid].score;
        let money = players[mysocketid].money;

        if (this.lastScore === score && this.lastMoney == money)
            return

        ctxUi.clearRect(0, 0, htmlCanvas.width, htmlCanvas.height);
        this.lastScore = score;
        ctxUi.font = "48px serif";
        ctxUi.fillText("Kills: " + score, 10, 50);

        this.lastMoney = money;
        ctxUi.font = "48px serif";
        ctxUi.fillText("Cash: " + money, 10, 100);

    }
}

class World {

    static attachToEvents() {

        window.addEventListener('resize', function () {
            World.resize();
        }, false);

        if (isMobile) {
            return;
        }

        document.addEventListener('keyup', (e) => {
            if (players[mysocketid] === undefined)
                return;

            if (e.code === "KeyW") socket.emit('keypress', { inputId: "w", state: false });
            else if (e.code === "KeyS") socket.emit('keypress', { inputId: "s", state: false });
            else if (e.code === "KeyA") socket.emit('keypress', { inputId: "a", state: false });
            else if (e.code === "KeyD") socket.emit('keypress', { inputId: "d", state: false });
            else if (e.code === "Space") socket.emit('keypress', { inputId: "attack", state: false });
        });

        document.addEventListener('keydown', (e) => {
            if (players[mysocketid] === undefined)
                return;

            if (e.code === "KeyW") socket.emit('keypress', { inputId: "w", state: true });
            else if (e.code === "KeyS") socket.emit('keypress', { inputId: "s", state: true });
            else if (e.code === "KeyA") socket.emit('keypress', { inputId: "a", state: true });
            else if (e.code === "KeyD") socket.emit('keypress', { inputId: "d", state: true });
            else if (e.code === "Digit1") socket.emit('keypress', { inputId: "switch_weapon", state: 1 })
            else if (e.code === "Digit2") socket.emit('keypress', { inputId: "switch_weapon", state: 2 })
            else if (e.code === "Digit3") socket.emit('keypress', { inputId: "switch_weapon", state: 3 })
            else if (e.code === "Digit4") socket.emit('keypress', { inputId: "switch_weapon", state: 4 })
            else if (e.code === "Digit5") socket.emit('keypress', { inputId: "switch_weapon", state: 5 })
            else if (e.code === "Digit6") socket.emit('keypress', { inputId: "switch_weapon", state: 6 })
        });

        document.addEventListener("mousedown", () => {
            if (players[mysocketid] === undefined)
                return;

            socket.emit('keypress', { inputId: "attack", state: true });
        })

        document.addEventListener("mouseup", () => {
            if (players[mysocketid] === undefined)
                return;

            socket.emit('keypress', { inputId: "attack", state: false });
        })

        document.addEventListener("mousemove", (e) => {
            if (players[mysocketid] === undefined)
                return;

            let x = -htmlCanvas.width / 2 + e.clientX
            let y = -htmlCanvas.height / 2 + e.clientY
            let angle = (Math.atan2(y, x) / Math.PI) * 180.0;
            players[mysocketid].angle = angle;
            socket.emit('keypress', { inputId: "mouseAngle", state: angle });
        });
    }

    static gameOverScreen() {
        document.getElementById("start").style.display = "block";
        document.getElementById("game").style.display = "none";

        let itemsHtml = document.getElementById("items");
        let buttons = itemsHtml.children;
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].remove();
        }

        // Remove elements from game.
        players = {};
        bullets = {};
        npcs = {};
        dropped_items = {};

        // Fuk it
        window.location.reload();
    }

    static start_screen() {
        document.getElementById("begin").addEventListener("click", () => {
            World.attachToEvents();
            socket = io("/game");
            World.connect_socket();
            let name = document.getElementById("player_name").value;
            if (name == "") {
                name = Math.random()
            }
            if (!isMobile) {
                socket.emit('start_game', name);
            } else {
                socket.emit('observer_connected');
            }
            document.getElementById("start").style.display = "none";
            document.getElementById("game").style.display = "block";
        });
    }

    static update() {
        for (const bullet in bullets) {
            bullets[bullet].update();
        }

        for (const player in players) {
            players[player].update();
        }

        for (const npc in npcs) {
            npcs[npc].update();
        }
    }

    static draw() {
        ctx.clearRect(0, 0, htmlCanvas.width, htmlCanvas.height);
        Game.drawMap();
        Game.drawEntities()
        if (!isMobile) {
            UI.draw()
        }
    }

    static resize() {
        htmlCanvas.width = window.innerWidth;
        htmlCanvas.height = window.innerHeight;

        htmlCanvasUi.width = window.innerWidth;
        htmlCanvasUi.height = window.innerHeight;
        UIStats.lastScore = -1;
        UIStats.lastMoney = -1;

        this.draw();
    }

    static mainLoop() {
        if (!isMobile) {
            if (players[mysocketid] === undefined) {
                World.gameOverScreen()
                return
            }
        }

        World.update();
        World.draw();
        requestAnimationFrame(World.mainLoop);
    }

    static connect_socket() {

        // Websocket stuff
        socket.on("player_disconnected", function (id) {
            delete players[id]
        });

        socket.on("player_connected", function (playerData) {
            new Player(playerData);
        });

        socket.on("init", function (data) {
            console.log("init", data)

            if (data.players) {
                for (const p of data.players) {
                    new Player(p);
                }
            }
            if (data.bullets) {
                for (const b of data.bullets) {
                    new Bullet(b);
                }
            }
            if (data.npcs) {
                for (const n of data.npcs) {
                    new NPC(n);
                }
            }

            if (data.dropped_items) {
                for (const i of data.dropped_items) {
                    new Item(i);
                }
            }

            // We got the player id, start the game.
            if (data.playerid) {
                mysocketid = data.playerid;

                // Used to set the size of the canvas
                World.resize();

                // Start the game loop
                World.mainLoop();
            }
        });

        socket.on("update", function (data) {
            // Players stuff
            if (data.players) {
                for (const playerData of data.players) {
                    let p = players[playerData.id];
                    if (p) {

                        if (playerData.x !== undefined) {
                            p.dx = playerData.x;
                        }

                        if (playerData.y !== undefined) {
                            p.dy = playerData.y;
                        }

                        if (playerData.score !== undefined) {
                            p.score = playerData.score;
                        }

                        if (playerData.hp !== undefined) {
                            p.hp = playerData.hp;
                        }

                        if (playerData.angle !== undefined) {
                            p.angle = playerData.angle;
                        }

                        if (playerData.money !== undefined) {
                            p.money = playerData.money;
                        }

                    }
                }
            }

            // Bullet stuff
            if (data.bullets) {
                for (const bd of data.bullets) {
                    let b = bullets[bd.id];
                    if (b) {
                        b.dx = bd.x;
                        b.dy = bd.y;
                    }
                }
            }
            if (data.npcs) {
                for (const npcData of data.npcs) {
                    let npc = npcs[npcData.id];
                    if (npc) {

                        if (npcData.x !== undefined) {
                            npc.dx = npcData.x;
                        }

                        if (npcData.y !== undefined) {
                            npc.dy = npcData.y;
                        }

                        if (npcData.hp !== undefined) {
                            npc.hp = npcData.hp;
                        }

                    }
                }
            }
        });

        socket.on("remove", function (data) {
            console.log("remove", data)

            if (data.players) {
                for (let i = 0; i < data.players.length; i++) {
                    delete players[data.players[i]];
                }
            }

            if (data.bullets) {
                for (let i = 0; i < data.bullets.length; i++) {
                    delete bullets[data.bullets[i]];
                }
            }

            if (data.npcs) {
                for (let i = 0; i < data.npcs.length; i++) {
                    delete npcs[data.npcs[i]];
                }
            }

            if (data.dropped_items) {
                for (let i = 0; i < data.dropped_items.length; i++) {
                    delete dropped_items[data.dropped_items[i]];
                }
            }
        });


        socket.on("item_grab", function (data) {
            console.log("Item grabbed: ", data)

            const newButton = document.createElement('button');
            newButton.textContent = data.name;
            newButton.id = data.id;
            let itemsHtml = document.getElementById("items");
            itemsHtml.appendChild(newButton);

            newButton.addEventListener('click', () => {
                socket.emit('keypress', { inputId: "use_item", state: data.id });
                let btn = document.getElementById(data.id);
                btn.parentElement.removeChild(btn);
            });
        });
    }
}

World.start_screen();

if (isMobile) {

    // Android
    document.addEventListener('touchstart', handleTouchStart, false);
    document.addEventListener('touchmove', handleTouchMove, false);

    var xDown = null;
    var yDown = null;
    var xUp = 0;
    var yUp = 0;
    function getTouches(evt) {
        return evt.touches ||             // browser API
            evt.originalEvent.touches; // jQuery
    }

    function handleTouchStart(evt) {
        const firstTouch = getTouches(evt)[0];
        xDown = world_x + firstTouch.clientX;
        yDown = world_y + firstTouch.clientY;
    };

    function handleTouchMove(evt) {
        if (!xDown || !yDown) {
            return;
        }

        xUp = evt.touches[0].clientX;
        yUp = evt.touches[0].clientY;
        var xDiff = xDown - xUp;
        var yDiff = yDown - yUp;

        world_x = xDiff;
        world_y = yDiff;
    };
}