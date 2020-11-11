import keyboard
import pygame

from game_settings import IMG_TANK2, PLAYER_MOVEMENT_SPEED, PLAYER_ROTATION_SPEED, TANK_CONTROLS, RELOAD_TIME
from tank import Tank


class Player(Tank):
    def __init__(self, game_map, starting_tile):
        super().__init__(game_map, IMG_TANK2, starting_tile, PLAYER_MOVEMENT_SPEED, PLAYER_ROTATION_SPEED)
        self.controls = TANK_CONTROLS

    def move_control(self):
        if self.alive:
            if keyboard.is_pressed(self.controls.rotate_left):
                self._rotate(self.rotation_speed)
            if keyboard.is_pressed(self.controls.rotate_right):
                self._rotate(-self.rotation_speed)
            if keyboard.is_pressed(self.controls.move_forward):
                self._move(self.movement_speed)
            if keyboard.is_pressed(self.controls.move_backward):
                self._move(-self.movement_speed)

    def shoot_control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls.shoot and self.alive:
                self.shoot()

    def get_reload_time(self):
        import time
        delta = time.time() - self.last_reload
        return RELOAD_TIME - delta if 0 <= delta <= RELOAD_TIME else 0.0
