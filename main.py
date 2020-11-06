from enum import Enum, auto

import pytmx as pytmx
from pygame.event import Event

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
        self.map_image = None

        self.game_state = GameState.GAME_ON

    def get_starting_positions(self, number):
        positions = []
        points = self.map.get_layer_by_name('Positions')
        map_positions = [(point.x + point.width / 2, point.y + point.height / 2, point.angle) for point in points]
        for _ in range(number):
            el = random.choice(map_positions)
            positions.append(el)
            map_positions.remove(el)
        return positions

    def set_map(self):
        number = random.randint(1, NUMBER_OF_MAP)
        self.map = pytmx.TiledMap('maps/map{0}.tmx'.format(str(number)))
        self.map_image = pygame.image.load('maps/map0{0}.jpg'.format(str(number)))

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
            if enemy.in_sight(self.player):
                enemy.shoot()

        for shell in shells:
            shell.move(SHELL_SPEED)
            for point in shell.points.values():
                if check_wall_collision(point, self.map_image):
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
        self.screen.blit(self.map_image, (0, 0))
        for tank in self.tanks:
            tank.draw(self.screen)
            for shell in tank.shells:
                shell.draw(self.screen)
        self.draw_text(str(len([e for e in self.enemies if e.alive])), BLACK, 60, (30, 10))

        if self.game_state != GameState.GAME_ON:
            self.draw_text(self.game_state.name, BLACK, 60, (WIDTH / 2, HEIGHT / 2 - 60))

        pygame.display.update()

    def draw_text(self, text, color, size, location):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = location
        self.screen.blit(text_surface, text_rect)

    def run(self):
        self.set_map()

        positions = self.get_starting_positions(NUMBER_OF_ENEMIES + 1)
        self.player = Player(self.map_image, positions[0][0], positions[0][1], positions[0][2])
        self.enemies = [Enemy(self.map_image, positions[i][0], positions[i][1], positions[i][2])
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
