import math
from math import sqrt

from game_settings import HEIGHT, WIDTH, TILE_SIZE


def to_radians(value):
    return value * (math.pi / 180)


def to_degrees(value):
    return value * (180 / math.pi)


def distance(point1, point2):
    return sqrt(abs(point1[0] - point2[0]) ** 2 + abs(point1[1] - point2[1]) ** 2)


def on_line(point, start, end) -> bool:
    return distance(start, point) + distance(end, point) == distance(start, end)


def inside_circle(point, center, radius) -> bool:
    return distance(point, center) < radius


def inside_square(point, x, y, width, height):
    return x < point[0] < x + width and y < point[1] < y + height


def get_angle(point, center):
    return math.atan2(point[1] - center[1], point[0] - center[0])


def invert(coordinates, invert_y: bool = True, invert_x: bool = False):
    x = (WIDTH - coordinates[0]) % WIDTH if invert_x else coordinates[0]
    y = (HEIGHT - coordinates[1]) % HEIGHT if invert_y else coordinates[1]
    return x, y


def inside_sector(point, center, radius, starting, ending) -> bool:
    angle = to_degrees(math.atan2(point[1] - center[1], point[0] - center[0])) % 360
    first_case = starting < ending and starting < angle < ending
    second_case = starting > ending and (angle > starting or angle < ending)
    return inside_circle(point, center, radius) and (first_case or second_case)


def check_wall_collision(point, game_map) -> bool:
    for x, y, tile in game_map.get_layer_by_name('Borders').tiles():
        cx, cy = x * TILE_SIZE, y * TILE_SIZE
        if inside_square(point, cx, cy, TILE_SIZE, TILE_SIZE):
            return True
    return False
