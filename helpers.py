import math
from math import sqrt

from game_settings import MAP


def check_wall_collision(point) -> bool:
    return 85 > MAP.get_at(point)[0] > 70


def to_radians(value):
    return value * (math.pi / 180)


def to_degrees(value):
    return value * (180 / math.pi)


def calculate_distance(pos1, pos2):
    return sqrt(abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2)
