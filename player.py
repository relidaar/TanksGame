import keyboard

from tank import Tank
from game_settings import *


class Player(Tank):
    def __init__(self, x_pos, y_pos, angle, controls: Controls):
        super().__init__(x_pos, y_pos, angle, IMG_TANK2)
        self.controls = controls
        self.score = 0

    def move_control(self):
        if self.alive:
            self.move_value = 0
            self.rotate_value = 0

            if keyboard.is_pressed(self.controls.rotate_left):
                self.rotate_value = ROTATION_DEGREE
            if keyboard.is_pressed(self.controls.rotate_right):
                self.rotate_value = -ROTATION_DEGREE
            if keyboard.is_pressed(self.controls.move_forward):
                self.move_value = MOVEMENT_DEGREE
            if keyboard.is_pressed(self.controls.move_backward):
                self.move_value = -MOVEMENT_DEGREE

            self.go(self.move_value)
            self.rotate(self.rotate_value)

    def shoot_control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls.shoot and self.alive:
                self.shoot()
