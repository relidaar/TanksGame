import math
import time

import pygame
from pygame import Surface

import collisions
from game_settings import SHELL_COUNT, SHELL_LIFE, EXPLOSION_TIME, IMG_EXPLOSION
from shell import Shell


class Tank:
    def __init__(self, tank_image, x, y, movement_speed, rotation_speed, angle=0):
        self.original_image = tank_image
        self.image = tank_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = self.get_location()
        self.movement_speed = movement_speed
        self.rotation_speed = rotation_speed
        self.angle = angle
        self.points = {}
        self.shells = []
        self.death = None
        self.alive = True

    def rotate(self, degree):
        self.angle += degree
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, value):
        self.points = {
            'right': [(self.rect.center[0] + 14, self.rect.center[1] - 14),
                      (self.rect.center[0] + 18, self.rect.center[1] - 7),
                      (self.rect.center[0] + 20, self.rect.center[1] + 0),
                      (self.rect.center[0] + 18, self.rect.center[1] + 7),
                      (self.rect.center[0] + 14, self.rect.center[1] + 14)],
            'top': [(self.rect.center[0] + 14, self.rect.center[1] + 14),
                    (self.rect.center[0] + 7, self.rect.center[1] + 18),
                    (self.rect.center[0] + 0, self.rect.center[1] + 20),
                    (self.rect.center[0] - 7, self.rect.center[1] + 18),
                    (self.rect.center[0] - 14, self.rect.center[1] + 14)],
            'left': [(self.rect.center[0] - 14, self.rect.center[1] + 14),
                     (self.rect.center[0] - 18, self.rect.center[1] + 7),
                     (self.rect.center[0] - 20, self.rect.center[1] + 0),
                     (self.rect.center[0] - 18, self.rect.center[1] - 7),
                     (self.rect.center[0] - 14, self.rect.center[1] - 14)],
            'bottom': [(self.rect.center[0] - 14, self.rect.center[1] - 14),
                       (self.rect.center[0] - 7, self.rect.center[1] - 18),
                       (self.rect.center[0] - 0, self.rect.center[1] - 20),
                       (self.rect.center[0] + 7, self.rect.center[1] - 18),
                       (self.rect.center[0] + 14, self.rect.center[1] - 14)]}

        angle_radian = (self.angle * (math.pi / 180))
        horizontal_move = -value * math.cos(angle_radian)
        vertical_move = value * math.sin(angle_radian)

        if self._horizontal_collision(horizontal_move):
            horizontal_move = 0
        if self._vertical_collision(vertical_move):
            vertical_move = 0

        self.x += horizontal_move
        self.y += vertical_move
        self.rect.center = (self.x, self.y)

    def _horizontal_collision(self, value):
        points = self.points['right'] if value >= 0 else self.points['left']
        return any(collisions.check_wall_collision(point) for point in points)

    def _vertical_collision(self, value):
        points = self.points['top'] if value >= 0 else self.points['bottom']
        return any(collisions.check_wall_collision(point) for point in points)

    def shoot(self):
        if len(self.shells) < SHELL_COUNT:
            self.shells.append(Shell(self.x, self.y, self.angle))

    def check_shells(self):
        now = time.time()
        self.shells = [shell for shell in self.shells if SHELL_LIFE > now - shell.time]

    def pop_shell(self, shell):
        if shell in self.shells:
            self.shells.remove(shell)

    def change_location(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def reset_shells(self):
        self.shells = []

    def draw(self, target: Surface):
        if self.alive or time.time() - self.death < EXPLOSION_TIME:
            target.blit(self.image, self.rect)

    def destroy(self):
        self.alive = False
        self.death = time.time()
        self.image = IMG_EXPLOSION

    def get_location(self):
        return self.x, self.y