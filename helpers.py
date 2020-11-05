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


def inside_circle(point, center, radius) -> bool:
    return calculate_distance(point, center) < radius


def get_angle(point, center) -> bool:
    return math.atan2(point[1] - center[1], point[0] - center[0])


def inside_sector(point, center, radius, starting, ending) -> bool:
    angle = to_degrees(get_angle(point, center))
    first_case = starting < ending and starting < angle < ending
    second_case = starting > ending and (angle > starting or angle < ending)
    return inside_circle(point, center, radius) and (first_case or second_case)
