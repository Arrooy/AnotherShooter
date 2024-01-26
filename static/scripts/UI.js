
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
        ctxUi.fillText("Gold: " + money, 10, 100);

    }
}
