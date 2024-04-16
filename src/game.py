import pyxel
import random
import time

from cloud_manager import CloudManager
from platform_manager import PlatformManager
from player_manager import PlayerManager

# 定数
DAYTIME_COLOR = 6
EVENING_COLOR = 15
NIGHT_COLOR = 5
MIDNIGHT_COLOR = 1

class Game:
    def __init__(self):
        self.init_pyxel()
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def init_pyxel(self):
        pyxel.init(160, 120, title="Climb Up")
        pyxel.load("../assets/pixels.pyxres")

    def reset_game(self):
        self.player_manager = PlayerManager()
        self.platform_manager = PlatformManager()
        self.cloud_manager = CloudManager()
        self.start_time = time.time()
        self.time_limit = 30
        self.end_time = None
        self.player_manager.reset()
        self.platform_manager.reset()
        self.cloud_manager.reset()

    def update(self):
        if self.player_manager.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        self.update_game_logic()

    def update_game_logic(self):
        self.check_time_limit()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player_manager.toggle_direction()
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.player_manager.can_climb(self.platform_manager.platforms):
                self.platform_manager.update_platforms(self.player_manager.direction)
                self.cloud_manager.update_clouds()
                self.player_manager.score += 1
            else:
                self.player_manager.game_over = True
                self.end_time = time.time()

    def toggle_direction(self):
        self.direction = 'left' if self.direction == 'right' else 'right'

    def draw(self):
        pyxel.cls(self.get_background_color())
        self.cloud_manager.draw(self.player_manager.score)
        self.platform_manager.draw()
        self.player_manager.draw()
        self.draw_score_and_time()
        if self.player_manager.game_over:
            sprite_w = 16 if self.player_manager.direction == 'right' else -16
            pyxel.blt(self.player_manager.player_x, self.player_manager.player_y, 0, 16, 0, sprite_w, 16)
            pyxel.text(50, 50, "Game Over", pyxel.COLOR_BLACK)
            pyxel.text(50, 60, "Press 'R' to Restart", pyxel.COLOR_BLACK)

    def draw_score_and_time(self):
        pyxel.text(5, 5, f"Score: {self.player_manager.score}", pyxel.COLOR_BLACK)
        elapsed_time = int(time.time() - self.start_time) if not self.player_manager.game_over else int(self.end_time - self.start_time)
        remaining_time = max(0, self.time_limit - elapsed_time)
        pyxel.text(120, 5, f"Time: {remaining_time}", pyxel.COLOR_BLACK)

    def check_time_limit(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.time_limit and not self.player_manager.game_over:
            self.player_manager.game_over = True
            self.end_time = time.time()  # タイムアップ時のタイムスタンプを記録

    def get_background_color(self) -> int:
        if(self.player_manager.score < 20):
            return DAYTIME_COLOR
        if(self.player_manager.score < 40):
            return EVENING_COLOR
        if (self.player_manager.score < 60):
            return NIGHT_COLOR
        return MIDNIGHT_COLOR

if __name__ == "__main__":
    Game()