
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

        this.drawRotatedPlayer(x, y);

        ctx.fillStyle = "black";
        ctx.font = "16px serif";
        ctx.textAlign = "center";
        ctx.fillText(this.name, x, y - 40);
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