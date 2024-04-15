import pyxel
import random
import time 

class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Climb Up")
        pyxel.load("../assets/pixels.pyxres")

        self.player_x = 72
        self.player_y = 88
        self.direction = 'right'
        self.score = 0
        self.game_over = False
        self.start_time = time.time()  # ゲーム開始時のタイムスタンプ
        self.time_limit = 30  # 制限時間を秒で設定

        self.platforms = [(self.player_x, self.player_y + 16)]
        self.initial_platforms()
        self.clouds = self.init_clouds()

        pyxel.run(self.update, self.draw)

    def init_clouds(self):
        clouds = []
        used_heights = []
        while len(clouds) < 4:
            # 16ピクセル単位で座標を生成する
            new_cloud_x = random.randint(0, (160 // 16) - 2) * 16  # 画面幅は160ピクセル、雲の幅は32ピクセル
            new_cloud_y = random.randint(0, (120 // 16) - 1) * 16  # 画面高さは120ピクセル、雲の高さは16ピクセル
            if new_cloud_y not in used_heights:
                clouds.append((new_cloud_x, new_cloud_y))
                used_heights.append(new_cloud_y)
        return clouds
    
    def is_overlapping(self, new_cloud, existing_cloud):
        nx, ny = new_cloud
        ex, ey = existing_cloud
        return nx < ex + 32 and nx + 32 > ex and ny < ey + 16 and ny + 16 > ey

    def initial_platforms(self):
        last_x, last_y = self.platforms[0]
        for _ in range(10):
            last_x += random.choice([-16, 16])
            last_y -= 16
            self.platforms.append((last_x, last_y))

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        self.check_time_limit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.direction = 'left' if self.direction == 'right' else 'right'

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.can_climb():
                self.climb()
            else:
                self.game_over = True
                self.end_time = time.time()

    def draw(self):
        pyxel.cls(6)
        for cloud_x, cloud_y in self.clouds:
            pyxel.blt(cloud_x, cloud_y, 0, 0, 48, 16, 16, pyxel.COLOR_YELLOW)
            pyxel.blt(cloud_x + 16, cloud_y, 0, 0, 48, -16, 16, pyxel.COLOR_YELLOW)
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, self.time_limit - elapsed_time)
        pyxel.text(130, 5, f"Time: {remaining_time}", pyxel.COLOR_BLACK)
        for x, y in self.platforms:
            pyxel.blt(x, y, 0, 32, 0, 16, 16, 6)

        if self.game_over:
            sprite_w = 16 if self.direction == 'right' else -16
            pyxel.blt(self.player_x, self.player_y, 0, 16, 0, sprite_w, 16)
            pyxel.text(50, 50, "Game Over", pyxel.COLOR_BLACK)
            pyxel.text(50, 60, "Press 'R' to Restart", pyxel.COLOR_BLACK)
        else:
            sprite_w = 16 if self.direction == 'right' else -16
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, sprite_w , 16)

        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_BLACK)
        current_time = self.end_time if self.game_over else time.time()
        elapsed_time = int(current_time - self.start_time)
        remaining_time = max(0, self.time_limit - elapsed_time)
        pyxel.text(130, 5, f"Time: {remaining_time}", pyxel.COLOR_BLACK)

    def check_time_limit(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.time_limit and not self.game_over:
            self.game_over = True
            self.end_time = time.time()  # タイムアップ時のタイムスタンプを記録


    def can_climb(self):
        next_x = self.player_x + (16 if self.direction == 'right' else -16)
        next_y = self.player_y
        return any(x == next_x and y == next_y for x, y in self.platforms)

    def climb(self):
        horizontal_shift = -16 if self.direction == 'right' else 16
        self.platforms = [(x + horizontal_shift, y + 16) for x, y in self.platforms]
        # 雲の位置を更新し、画面外に出た雲を処理する
        self.clouds = [(x, y + 16) for x, y in self.clouds]
        self.clouds = [cloud for cloud in self.clouds if cloud[1] < 120]
        while len(self.clouds) < 4:
            self.add_cloud()
        self.score += 1
        self.add_platform()

    def add_cloud(self):
        new_cloud = (random.randint(0, 128), 0)
        while any(self.is_overlapping(new_cloud, cloud) for cloud in self.clouds):
            new_cloud = (random.randint(0, 128), 0)
        self.clouds.append(new_cloud)

    def add_platform(self):
        last_x, last_y = self.platforms[-1]
        new_x = random.choice([last_x + 16, last_x - 16])
        new_y = last_y - 16
        self.platforms.append((new_x, new_y))

    def reset_game(self):
        self.player_x = 72
        self.player_y = 88
        self.direction = 'right'
        self.score = 0
        self.game_over = False
        self.start_time = time.time()
        self.end_time = None
        self.platforms = [(self.player_x, self.player_y + 16)]
        self.initial_platforms()
        self.clouds = self.init_clouds()


Game()