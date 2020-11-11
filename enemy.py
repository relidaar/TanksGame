import random
from math import ceil, floor

from game_settings import IMG_TANK1, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, ENEMY_FOV_DISTANCE, ENEMY_FOV, TILES_X, \
    TILES_Y
from helpers import inside_sector, invert, get_angle, four_neighbors
from player import Player
from tank import Tank
from tile import Tile


class Enemy(Tank):
    def __init__(self, game_map, tiles, starting_tile):
        super().__init__(game_map, IMG_TANK1, starting_tile, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED)
        self.tiles = tiles
        self.previous = [starting_tile, starting_tile]
        self.turned = False
        self.last_movement = 0
        self.path = []
        self._get_next_tile()

    def in_sight(self, player: Player) -> bool:
        if not player.alive: return False
        start_angle = (self.angle - ENEMY_FOV / 2) % 360
        end_angle = (self.angle + ENEMY_FOV / 2) % 360
        point = invert(player.get_location())
        center = invert(self.get_location())
        return inside_sector(point, center, ENEMY_FOV_DISTANCE, start_angle, end_angle)

    def move_to(self, target):
        pass

    def move(self):
        if not self.alive: return

        self._rotate_to_target()

        if not self.turned: return

        if not self._on_next():
            self._move(self.movement_speed)
            return

        self.turned = False
        self.previous = self.previous[1:]
        self.previous.append(self.path[0])
        self.path = []
        self._get_next_tile()

    def _rotate_to_target(self):
        if not self.alive: return
        if self.turned: return
        tile = self.path[0]
        if floor(tile.angle) <= self.angle <= ceil(tile.angle):
            self.turned = True
            return

        if tile.angle < self.angle < tile.angle + 180:
            self._rotate(-self.rotation_speed)
        else:
            self._rotate(self.rotation_speed)

    def _on_next(self):
        coords = self.path[0].get_pos()
        return floor(coords[0]) <= self.x <= ceil(coords[0]) and floor(coords[1]) <= self.y <= ceil(coords[1])

    def _get_next_tile(self):
        current = self.previous[-1].get_indices()
        previous = self.previous[0].get_indices()

        tiles = four_neighbors(TILES_X, TILES_Y, current[0], current[1])
        tiles = [tile for tile in tiles if tile in self.tiles.keys()]
        if len(tiles) > 1:
            tiles = [tile for tile in tiles if tile != previous]

        tile = self.tiles[random.choice(tiles)]
        angle = get_angle(invert(tile.get_pos()), invert(self.get_location()))
        self.path.append(Tile(tile.get_pos(), tile.get_indices(), angle))
