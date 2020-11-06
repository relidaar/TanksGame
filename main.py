import random
from enum import Enum, auto

from pygame.event import Event
from pytmx import load_pygame

from enemy import Enemy
from game_settings import *
from helpers import check_wall_collision
from player import Player


class GameState(Enum):
    DEFEAT = auto()
    VICTORY = auto()
    DRAW = auto()
    GAME_ON = auto()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = None
        self.enemies = []
        self.tanks = []
        self.map = None
        self.tiles = dict()
        self.coords = dict()

        self.game_state = GameState.GAME_ON

    def get_starting_positions(self, number):
        positions = []
        points = list(self.tiles.values())
        for _ in range(number + 1):
            el = random.choice(points)
            if el not in positions:
                positions.append(el)
        return positions

    def set_map(self):
        number = random.randint(1, NUMBER_OF_MAPS)
        self.map = load_pygame('maps/map{0}.tmx'.format(str(number)))

    def process(self, event: Event):
        if event.type == pygame.QUIT:
            self.running = False
        self.player.shoot_control(event)

    def update(self):
        if self.game_state != GameState.GAME_ON:
            return

        if not self.player.alive and all(not e.alive for e in self.enemies):
            self.game_state = GameState.DRAW
            return

        if not self.player.alive:
            self.game_state = GameState.DEFEAT
            return

        if all(not e.alive for e in self.enemies):
            self.game_state = GameState.VICTORY
            return

        self.player.move_control()

        shells = []
        for tank in self.tanks:
            tank.check_shells()
            shells += tank.shells

        for enemy in self.enemies:
            enemy.rotate()
            enemy.move()
            if enemy.in_sight(self.player):
                enemy.shoot()

        for shell in shells:
            shell.move(SHELL_SPEED)
            for point in shell.points.values():
                if check_wall_collision(point, self.map):
                    for shooting_tank in self.tanks:
                        shooting_tank.pop_shell(shell)

            if shell in self.player.shells:
                for enemy in self.enemies:
                    if shell.collides(enemy):
                        enemy.destroy()
                        self.player.pop_shell(shell)
            if any(shell in e.shells for e in self.enemies):
                if shell.collides(self.player):
                    self.player.destroy()
                    for shooting_tank in self.tanks:
                        shooting_tank.pop_shell(shell)

    def draw(self):
        self.draw_map()
        for tank in self.tanks:
            tank.draw(self.screen)
            for shell in tank.shells:
                shell.draw(self.screen)
        self.draw_text(str(len([e for e in self.enemies if e.alive])), WHITE, 60, (15, 10))

        if self.game_state != GameState.GAME_ON:
            self.draw_text(self.game_state.name, BLACK, 60, (WIDTH / 2, HEIGHT / 2 - 60))

        pygame.display.update()

    def draw_map(self):
        for layer in [layer for layer in self.map.layers if layer.Type == 'Tiles']:
            for x, y, tile in layer.tiles():
                self.screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

    def draw_text(self, text, color, size, location):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = location
        self.screen.blit(text_surface, text_rect)

    def run(self):
        self.set_map()
        self.tiles = dict()
        self.coords = dict()
        for row, col, _ in self.map.get_layer_by_name('Path').tiles():
            pos = (row * TILE_SIZE + TILE_SIZE / 2, col * TILE_SIZE + TILE_SIZE / 2)
            self.tiles[(row, col)] = pos
            self.coords[pos] = (row, col)

        positions = self.get_starting_positions(NUMBER_OF_ENEMIES + 1)
        self.player = Player(self.map, positions[0][0], positions[0][1])
        self.enemies = [Enemy(self.map, self.tiles, self.coords, positions[i][0], positions[i][1])
                        for i in range(1, NUMBER_OF_ENEMIES + 1)]

        self.tanks = [self.player]
        self.tanks.extend(self.enemies)

        for tank in self.tanks:
            tank.reset_shells()

        while self.running:
            for event in pygame.event.get():
                self.process(event)
            self.update()
            self.draw()
            self.clock.tick(60)

    def cleanup(self):
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
    game.cleanup()
