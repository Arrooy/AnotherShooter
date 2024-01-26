
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