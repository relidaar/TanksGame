import time
from math import sqrt

from game_settings import *


def check_wall_collision(point):
    return 85 > MAP.get_at(point)[0] > 70


def check_collision(shell, tank):
    passing_time = time.time() - shell.time
    distance = calculate_distance(tank.get_location(), shell.get_center_location())
    return passing_time > 0.3 and distance <= SHELL_RADIUS + TANK_RADIUS


def calculate_distance(pos1: (float, float), pos2: (float, float)):
    return sqrt(abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2)
