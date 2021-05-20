import pygame


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

TILE_SIZE = 24
TILES_X = 22
TILES_Y = 24
NUMBER_OF_MAPS = 3
WIDTH, HEIGHT = TILES_X * TILE_SIZE, TILES_Y * TILE_SIZE
GAME_TITLE = "Tanks!"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SHELL_RADIUS = 5
SHELL_LIFE = 1
SHELL_COUNT = 1
SHELL_SPEED = 4

RELOAD_TIME = 3
EXPLOSION_TIME = 0.3
TANK_RADIUS = int(TILE_SIZE * 0.4)

PLAYER_MOVEMENT_SPEED = 2
PLAYER_ROTATION_SPEED = 3

ENEMY_MOVEMENT_SPEED = 1
ENEMY_ROTATION_SPEED = 2
ENEMY_FOV = 20
ENEMY_FOV_DISTANCE = 150
NUMBER_OF_ENEMIES = 5
