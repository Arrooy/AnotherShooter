
class NPC extends ColisionEntity {
    constructor(initPack) {
        super(initPack);
        npcs[this.id] = this;
        this.angle = 0
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
        //ctx.fillRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
        //ctx.strokeRect(x - this.size / 2, y - this.size / 2, this.size, this.size);
        this.drawRotatedPlayer(x,y);
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

        // NPC
        let nx = -width / 2;
        let ny = -height / 2;
        ctx.fillStyle = "brown";
        ctx.fillRect(nx, ny, width, height);
        ctx.strokeRect(nx, ny, width, height);

        ctx.fillStyle = "brown";
        ctx.beginPath();
        ctx.arc(nx + width - 1, ny + height, 20, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.fill()

        ctx.beginPath();
        ctx.arc(nx + width - 1, ny, 20, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.fill();

        // restore the context to its untranslated/unrotated state
        ctx.restore();

    }
}