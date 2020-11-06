import random
from math import ceil, floor

from game_settings import IMG_TANK1, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, ENEMY_FOV_DISTANCE, ENEMY_FOV, TILES_X, \
    TILES_Y
from helpers import inside_sector, invert, get_angle, four_neighbors
from player import Player
from tank import Tank


class Enemy(Tank):
    def __init__(self, game_map, tiles, coords, x, y, angle=0):
        super().__init__(game_map, IMG_TANK1, x, y, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, angle)
        self.tiles = tiles
        self.previous = coords[(x, y)]
        self.current = coords[(x, y)]
        self.next, self.target_angle = self._get_next_tile()
        self.turned = False
        self.last_movement = 0

    def in_sight(self, player: Player) -> bool:
        if not player.alive: return False
        start_angle = (self.angle - ENEMY_FOV / 2) % 360
        end_angle = (self.angle + ENEMY_FOV / 2) % 360
        point = invert(player.get_location())
        center = invert(self.get_location())
        return inside_sector(point, center, ENEMY_FOV_DISTANCE, start_angle, end_angle)

    def move(self):
        if not self.alive: return
        if not self.turned: return
        if not self._on_next():
            self._move(self.movement_speed)
            return

        self.turned = False
        self.previous = tuple(self.current)
        self.current = tuple(self.next)
        self.next, self.target_angle = self._get_next_tile()

    def rotate(self):
        if not self.alive: return
        if self.turned: return
        if floor(self.target_angle) <= self.angle <= ceil(self.target_angle):
            self.turned = True
            return

        if self.target_angle < self.angle < self.target_angle + 180:
            self._rotate(-self.rotation_speed)
        else:
            self._rotate(self.rotation_speed)

    def _on_next(self):
        coords = self.tiles[self.next]
        return floor(coords[0]) <= self.x <= ceil(coords[0]) and floor(coords[1]) <= self.y <= ceil(coords[1])

    def _get_next_tile(self):
        tiles = four_neighbors(TILES_X, TILES_Y, self.current[0], self.current[1])
        tiles = [tile for tile in tiles if tile in self.tiles.keys()]
        tiles = [tile for tile in tiles if tile != self.previous] if len(tiles) > 1 else tiles
        next_tile = random.choice(tiles)
        target_angle = get_angle(invert(self.tiles[next_tile]), invert(self.get_location()))
        return next_tile, target_angle
