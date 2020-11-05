from tank import Tank
from game_settings import IMG_TANK1


class Enemy(Tank):
    def __init__(self, x, y, movement_speed, rotation_speed, angle=0):
        super().__init__(IMG_TANK1, x, y, movement_speed, rotation_speed, angle)