import math
import time

import pygame
from pygame import Surface

from helpers import distance, to_radians
from game_settings import SHELL_RADIUS, TANK_RADIUS, BLACK
from tank import Tank


class Shell:
    def __init__(self, x, y, angle):
        self.angle = angle
        angle_radian = (self.angle * (math.pi / 180))
        self.x = x + (TANK_RADIUS - SHELL_RADIUS + 2) * math.cos(angle_radian)
        self.y = y - (TANK_RADIUS - SHELL_RADIUS + 2) * math.sin(angle_radian)
        self.time = time.time()
        self.points = dict()

    def move(self, value):
        x, y = self.get_location()
        self.points = {
            "right": (x + SHELL_RADIUS, y + 0),
            "top": (x + 0, y + SHELL_RADIUS),
            "left": (x - SHELL_RADIUS, y - 0),
            "bottom": (x - 0, y - SHELL_RADIUS)
        }

        angle_radian = to_radians(self.angle)
        self.x += value * math.cos(angle_radian)
        self.y += -value * math.sin(angle_radian)

    def get_location(self):
        return int(self.x), int(self.y)

    def draw(self, target: Surface):
        return pygame.draw.circle(target, BLACK, self.get_location(), SHELL_RADIUS)

    def collides(self, tank: Tank) -> bool:
        passing_time = time.time() - self.time
        dist = distance(tank.get_location(), self.get_location())
        return tank.alive and passing_time > 0.1 and dist <= SHELL_RADIUS + TANK_RADIUS
