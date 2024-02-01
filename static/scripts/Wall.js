
class Wall{
    constructor(initPack) {
        this.id = initPack.id;
        this.x = initPack.x;
        this.y = initPack.y;
        this.w = initPack.w;
        this.h = initPack.h;
        this.color = initPack.color;

        walls[this.id] = this;
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
        ctx.fillRect(x, y, this.w, this.h);
        ctx.strokeRect(x, y, this.w, this.h);
    }
}