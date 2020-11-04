import time

from pygame import Surface

from collisions import check_wall_collision
from game_settings import *
from shell import Shell


class Tank:
    def __init__(self, x_pos, y_pos, angle, tank_image):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.original_image = tank_image
        self.image = tank_image
        self.angle = angle
        self.rect = self.image.get_rect().move(self.get_location())
        self.points = {}
        self.shells = []
        self.death = None

        self.vertical_move = 0
        self.horizontal_move = 0
        self.rotate_value = 0
        self.move_value = 0
        self.alive = True

    def rotate(self, degree):
        self.angle += degree
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def go(self, value):
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
        self.horizontal_move = -value * math.cos(angle_radian)
        self.vertical_move = value * math.sin(angle_radian)

        if self._horizontal_collision(self.horizontal_move):
            self.horizontal_move = 0
        if self._vertical_collision(self.vertical_move):
            self.vertical_move = 0

        self.x_pos += self.horizontal_move
        self.y_pos += self.vertical_move
        self.rect.center = (self.x_pos, self.y_pos)

    def _horizontal_collision(self, value):
        points = self.points['right'] if value >= 0 else self.points['left']
        return any(check_wall_collision(point) for point in points)

    def _vertical_collision(self, value):
        points = self.points['top'] if value >= 0 else self.points['bottom']
        return any(check_wall_collision(point) for point in points)

    def shoot(self):
        if len(self.shells) < SHELL_COUNT:
            self.shells.append(Shell(self.x_pos, self.y_pos, self.angle))

    def check_shells(self):
        now = time.time()
        self.shells = [shell for shell in self.shells if SHELL_LIFE > now - shell.time]

    def pop_shell(self, shell):
        if shell in self.shells:
            self.shells.remove(shell)

    def change_location(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def reset_shells(self):
        self.shells = []

    def draw(self, target: Surface):
        target.blit(self.image, self.rect)

    def destroy(self):
        self.death = time.time()
        self.image = IMG_EXPLOSION

    def get_location(self):
        return self.x_pos, self.y_pos
