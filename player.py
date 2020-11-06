import keyboard
import pygame

from game_settings import IMG_TANK2, PLAYER_MOVEMENT_SPEED, PLAYER_ROTATION_SPEED, TANK_CONTROLS
from tank import Tank


class Player(Tank):
    def __init__(self, game_map, x, y, angle=0):
        super().__init__(game_map, IMG_TANK2, x, y, PLAYER_MOVEMENT_SPEED, PLAYER_ROTATION_SPEED, angle)
        self.controls = TANK_CONTROLS

    def move_control(self):
        if self.alive:
            if keyboard.is_pressed(self.controls.rotate_left):
                self.rotate(self.rotation_speed)
            if keyboard.is_pressed(self.controls.rotate_right):
                self.rotate(-self.rotation_speed)
            if keyboard.is_pressed(self.controls.move_forward):
                self.move(self.movement_speed)
            if keyboard.is_pressed(self.controls.move_backward):
                self.move(-self.movement_speed)

    def shoot_control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls.shoot and self.alive:
                self.shoot()
