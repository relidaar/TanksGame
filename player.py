import keyboard
import pygame

from game_settings import Controls, IMG_TANK2
from tank import Tank


class Player(Tank):
    def __init__(self, controls: Controls, x, y, movement_speed, rotation_speed, angle=0):
        super().__init__(IMG_TANK2, x, y, movement_speed, rotation_speed, angle)
        self.controls = controls

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
