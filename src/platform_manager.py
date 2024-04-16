import random

import pyxel


class PlatformManager:
    def __init__(self):
        self.platforms = [(72, 104)]
        self.create_initial_platforms()

    def draw(self):
        for x, y in self.platforms:
            pyxel.blt(x, y, 0, 32, 0, 16, 16, 0)

    def create_initial_platforms(self):
        last_x, last_y = self.platforms[0]
        for _ in range(10):
            last_x += random.choice([-16, 16])
            last_y -= 16
            self.platforms.append((last_x, last_y))

    def update_platforms(self, direction):
        horizontal_shift = -16 if direction == 'right' else 16
        self.platforms = [(x + horizontal_shift, y + 16) for x, y in self.platforms]
        self.platforms = [p for p in self.platforms if p[1] < 120]  # 画面外に出た足場を削除
        self.add_platform()

    def add_platform(self):
        last_x, last_y = self.platforms[-1]
        new_x = random.choice([last_x + 16, last_x - 16])
        new_y = last_y - 16
        self.platforms.append((new_x, new_y))

    def reset(self):
        self.platforms = [(72, 104)]
        self.create_initial_platforms()