import math
import random

import pygame

NUMBER_OF_MAP = 3
NUMBER_OF_POSITIONS = 13
MAP_NUMBER = random.randint(1, NUMBER_OF_MAP)
MAP = pygame.image.load('maps/map0{0}.jpg'.format(str(MAP_NUMBER)))
TANK_POSSIBLE_POSITIONS = ((50, 50),
                           (650, 650),
                           (650, 50),
                           (45, 565),
                           (650, 480),
                           (390, 125),
                           (225, 390),
                           (125, 395),
                           (480, 220),
                           (300, 650),
                           (560, 395),
                           (210, 45),
                           (45, 315))

IMG_TANK1 = pygame.image.load('img/tank1.png')
IMG_TANK2 = pygame.image.load('img/tank2.png')
IMG_TANK3 = pygame.image.load('img/tank3.png')
IMG_EXPLOSION = pygame.image.load('img/explosion.png')


class Controls:
    def __init__(self, move_forward, move_backward, rotate_left, rotate_right, shoot):
        self.move_forward = move_forward
        self.move_backward = move_backward
        self.rotate_left = rotate_left
        self.rotate_right = rotate_right
        self.shoot = shoot


TANK_CONTROLS = Controls('w', 's', 'a', 'd', pygame.K_SPACE)

WIDTH, HEIGHT = 700, 700
GAME_TITLE = "Tanks!"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SHELL_RADIUS = 10
SHELL_LIFE = 1
SHELL_COUNT = 1
SHELL_SPEED = 4

RELOAD_TIME = 3
EXPLOSION_TIME = 0.5
TANK_RADIUS = 25

PLAYER_MOVEMENT_SPEED = 2
PLAYER_ROTATION_SPEED = 3

ENEMY_MOVEMENT_SPEED = 1
ENEMY_ROTATION_SPEED = 3
ENEMY_FOV = 35
ENEMY_FOV_DISTANCE = 200
NUMBER_OF_ENEMIES = 1
