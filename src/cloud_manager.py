import random

import pyxel


class CloudManager:
    def __init__(self):
        self.clouds = self.create_initial_clouds()

    def draw(self, score: int):
        for cloud_x, cloud_y, type in self.clouds:
            if (score < 60):
                pyxel.blt(cloud_x, cloud_y, 0, 0, 48, 16, 16, 0)
                pyxel.blt(cloud_x + 16, cloud_y, 0, 0, 48, -16, 16, 0)
            else:
                pyxel.blt(cloud_x, cloud_y, 0, (type + 1) * 16, 48, 16, 16, 0)

    def create_initial_clouds(self):
        clouds = []
        used_heights = []
        while len(clouds) < 4:
            new_cloud_x = random.randint(0, 140)
            new_cloud_y = random.randint(0, 104)
            new_cloud_type = random.randint(0, 2)
            if new_cloud_y not in used_heights:
                clouds.append((new_cloud_x, new_cloud_y, new_cloud_type))
                used_heights.append(new_cloud_y)
        return clouds

    def update_clouds(self):
        self.clouds = [(x, y + 16, type) for x, y, type in self.clouds if y + 16 < 120]
        while len(self.clouds) < 4:
            self.add_cloud()

    def add_cloud(self):
        new_cloud = (random.randint(0, 128), 0, random.randint(0, 2))
        self.clouds.append(new_cloud)

    def reset(self):
        self.clouds = self.create_initial_clouds()