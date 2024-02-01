
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

        for (const wall in walls) {
            walls[wall].draw();
        }
        
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