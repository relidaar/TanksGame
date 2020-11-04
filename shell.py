import time

from pygame import Surface

from game_settings import *


class Shell:
    def __init__(self, x, y, angle):
        self.y_pos = y
        self.angle = angle
        angle_radian = (self.angle * (math.pi / 180))
        self.x_pos = x - (TANK_RADIUS - SHELL_RADIUS + 2) * math.cos(angle_radian)
        self.y_pos = y + (TANK_RADIUS - SHELL_RADIUS + 2) * math.sin(angle_radian)
        self.vertical_move = 0
        self.horizontal_move = 0
        self.time = time.time()
        self.points = dict()
        self.horizontal_neg = 1
        self.vertical_neg = 1

    def move(self, value):
        x = int(self.x_pos)
        y = int(self.y_pos)

        self.points = {
            "right": (x + SHELL_RADIUS, y + 0),
            "top": (x + 0, y + SHELL_RADIUS),
            "left": (x - SHELL_RADIUS, y - 0),
            "bottom": (x - 0, y - SHELL_RADIUS)
        }

        angle_radian = (self.angle * (math.pi / 180))

        self.horizontal_move = self.horizontal_neg * -value * math.cos(angle_radian)
        self.vertical_move = self.vertical_neg * value * math.sin(angle_radian)

        self.x_pos += self.horizontal_move
        self.y_pos += self.vertical_move

    def get_center_location(self):
        return int(self.x_pos), int(self.y_pos)

    def draw(self, target: Surface):
        return pygame.draw.circle(target, BLACK, self.get_center_location(), SHELL_RADIUS)
