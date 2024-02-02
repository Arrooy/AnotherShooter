
class Wall extends ColisionEntity{
    constructor(initPack) {
        super(initPack);
        this.w = initPack.w;
        this.h = initPack.h;
        this.size = initPack.h/2;
        this.color = initPack.color;
        
        if (initPack.visible === undefined){
            this.visible = true;
        }else{
            this.visible = initPack.visible;
        }

        walls[this.id] = this;
    }

    draw() {
        if(!this.visible) return;

        let x, y;
        if (!isMobile) {
            x = this.x - players[mysocketid].x + htmlCanvas.width / 2;
            y = this.y - players[mysocketid].y + htmlCanvas.height / 2;
        } else {
            x = world_x + this.x;
            y = world_y + this.y;
        }

        super.drawHpBar(x + this.w/2, y + this.h/2);
        ctx.fillStyle = this.color;
        ctx.fillRect(x, y, this.w, this.h);
        ctx.strokeRect(x, y, this.w, this.h);
    }
}