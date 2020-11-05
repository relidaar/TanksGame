import time
from math import sqrt

from game_settings import SHELL_RADIUS, TANK_RADIUS, MAP
from shell import Shell
from tank import Tank


def check_wall_collision(point) -> bool:
    return 85 > MAP.get_at(point)[0] > 70


def check_collision(shell: Shell, tank: Tank) -> bool:
    passing_time = time.time() - shell.time
    distance = calculate_distance(tank.get_location(), shell.get_location())
    return passing_time > 0.3 and distance <= SHELL_RADIUS + TANK_RADIUS


def calculate_distance(pos1, pos2):
    return sqrt(abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2)
