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
    return to_degrees(math.atan2(point[1] - center[1], point[0] - center[0])) % 360


def invert(coordinates, invert_y: bool = True, invert_x: bool = False):
    x = (WIDTH - coordinates[0]) % WIDTH if invert_x else coordinates[0]
    y = (HEIGHT - coordinates[1]) % HEIGHT if invert_y else coordinates[1]
    return x, y


def four_neighbors(width, height, row, col):
    ans = []
    if row > 0:
        ans.append((row - 1, col))
    if row < height - 1:
        ans.append((row + 1, col))
    if col > 0:
        ans.append((row, col - 1))
    if col < width - 1:
        ans.append((row, col + 1))
    return ans


def eight_neighbors(width, height, row, col):
    ans = four_neighbors(width, height, row, col)
    if (row > 0) and (col > 0):
        ans.append((row - 1, col - 1))
    if (row > 0) and (col < width - 1):
        ans.append((row - 1, col + 1))
    if (row < height - 1) and (col > 0):
        ans.append((row + 1, col - 1))
    if (row < height - 1) and (col < width - 1):
        ans.append((row + 1, col + 1))
    return ans


def inside_sector(point, center, radius, starting, ending) -> bool:
    angle = get_angle(point, center)
    first_case = starting < ending and starting < angle < ending
    second_case = starting > ending and (angle > starting or angle < ending)
    return inside_circle(point, center, radius) and (first_case or second_case)


def check_wall_collision(point, game_map) -> bool:
    for x, y, tile in game_map.get_layer_by_name('Borders').tiles():
        cx, cy = x * TILE_SIZE, y * TILE_SIZE
        if inside_square(point, cx, cy, TILE_SIZE, TILE_SIZE):
            return True
    return False
