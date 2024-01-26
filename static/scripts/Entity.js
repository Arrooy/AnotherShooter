
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
