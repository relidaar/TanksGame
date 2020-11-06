import math
import time

import pygame
from pygame import Surface

import helpers
from game_settings import SHELL_COUNT, SHELL_LIFE, EXPLOSION_TIME, IMG_EXPLOSION, RELOAD_TIME, TANK_RADIUS


class Tank:
    def __init__(self, game_map, tank_image: Surface, x, y, movement_speed, rotation_speed, angle=0):
        self.game_map = game_map

        self.size = TANK_RADIUS * 2 + 10
        self.original_image = pygame.transform.rotate(pygame.transform.scale(tank_image, (self.size, self.size)), 180)
        self.image = pygame.transform.rotate(self.original_image, angle % 360)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.center = self.get_location()

        self.movement_speed = movement_speed
        self.rotation_speed = rotation_speed
        self.angle = angle

        self.points = {}
        self.shells = []
        self.last_reload = 0

        self.death = None
        self.alive = True

    def _rotate(self, degree):
        if not self.alive: return
        self.angle += degree
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def _calculate_points(self):
        values = [
            TANK_RADIUS - 6, TANK_RADIUS - 2, TANK_RADIUS,
            int(TANK_RADIUS * 0.7), int(TANK_RADIUS * 0.35), 0
        ]
        self.points = {
            'right': [(self.rect.center[0] + values[0], self.rect.center[1] - values[3]),
                      (self.rect.center[0] + values[1], self.rect.center[1] - values[4]),
                      (self.rect.center[0] + values[2], self.rect.center[1] + values[5]),
                      (self.rect.center[0] + values[1], self.rect.center[1] + values[4]),
                      (self.rect.center[0] + values[2], self.rect.center[1] + values[3])],
            'top': [(self.rect.center[0] + values[3], self.rect.center[1] + values[0]),
                    (self.rect.center[0] + values[4], self.rect.center[1] + values[1]),
                    (self.rect.center[0] + values[5], self.rect.center[1] + values[2]),
                    (self.rect.center[0] - values[4], self.rect.center[1] + values[1]),
                    (self.rect.center[0] - values[3], self.rect.center[1] + values[2])],
            'left': [(self.rect.center[0] - values[0], self.rect.center[1] + values[3]),
                     (self.rect.center[0] - values[1], self.rect.center[1] + values[4]),
                     (self.rect.center[0] - values[2], self.rect.center[1] + values[5]),
                     (self.rect.center[0] - values[1], self.rect.center[1] - values[4]),
                     (self.rect.center[0] - values[2], self.rect.center[1] - values[3])],
            'bottom': [(self.rect.center[0] - values[3], self.rect.center[1] - values[0]),
                       (self.rect.center[0] - values[4], self.rect.center[1] - values[1]),
                       (self.rect.center[0] - values[5], self.rect.center[1] - values[2]),
                       (self.rect.center[0] + values[4], self.rect.center[1] - values[1]),
                       (self.rect.center[0] + values[3], self.rect.center[1] - values[2])]}

    def _move(self, value):
        if not self.alive: return
        self._calculate_points()

        angle_radian = helpers.to_radians(self.angle)
        horizontal_move = value * math.cos(angle_radian)
        vertical_move = -value * math.sin(angle_radian)

        if self._horizontal_collision(horizontal_move):
            horizontal_move = 0
        if self._vertical_collision(vertical_move):
            vertical_move = 0

        self.x += horizontal_move
        self.y += vertical_move
        self.rect.center = (self.x, self.y)

    def _horizontal_collision(self, value):
        points = self.points['right'] if value >= 0 else self.points['left']
        return any(helpers.check_wall_collision(point, self.game_map) for point in points)

    def _vertical_collision(self, value):
        points = self.points['top'] if value >= 0 else self.points['bottom']
        return any(helpers.check_wall_collision(point, self.game_map) for point in points)

    def shoot(self):
        if not self.alive: return
        import shell
        now = time.time()
        if len(self.shells) < SHELL_COUNT and now - self.last_reload > RELOAD_TIME:
            self.shells.append(shell.Shell(self.x, self.y, self.angle))
            self.last_reload = now

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
