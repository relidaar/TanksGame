from helpers import inside_sector
from player import Player
from tank import Tank
from game_settings import IMG_TANK1, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, ENEMY_FOV_DISTANCE, ENEMY_FOV


class Enemy(Tank):
    def __init__(self, x, y, angle=0):
        super().__init__(IMG_TANK1, x, y, ENEMY_MOVEMENT_SPEED, ENEMY_ROTATION_SPEED, angle)

    def in_sight(self, player: Player):
        return True

