from helpers import inside_sector, invert
from player import Player
from tank import Tank
from game_settings import IMG_TANK1, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, ENEMY_FOV_DISTANCE, ENEMY_FOV


class Enemy(Tank):
    def __init__(self, x, y, angle=0):
        super().__init__(IMG_TANK1, x, y, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, angle)

    def in_sight(self, player: Player) -> bool:
        if not player.alive: return False
        start_angle = (self.angle - ENEMY_FOV / 2) % 360
        end_angle = (self.angle + ENEMY_FOV / 2) % 360
        point = invert(player.get_location())
        center = invert(self.get_location())
        return inside_sector(point, center, ENEMY_FOV_DISTANCE, start_angle, end_angle)

