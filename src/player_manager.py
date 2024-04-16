import pyxel


class PlayerManager:
    def __init__(self):
        self.player_x = 72
        self.player_y = 88
        self.direction = 'right'
        self.score = 0
        self.game_over = False

    def draw(self):
        sprite_w = 16 if self.direction == 'right' else -16
        sprite_x = 16 if self.game_over else 0
        pyxel.blt(self.player_x, self.player_y, 0, sprite_x, 0, sprite_w, 16)

    def toggle_direction(self):
        self.direction = 'left' if self.direction == 'right' else 'right'

    def can_climb(self, platforms):
        next_x = self.player_x + (16 if self.direction == 'right' else -16)
        next_y = self.player_y
        return any(x == next_x and y == next_y for x, y in platforms)
    
    def reset(self):
        self.player_x = 72
        self.player_y = 88
        self.direction = 'right'
        self.score = 0
        self.game_over = False