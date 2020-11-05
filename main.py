from enum import Enum, auto

from pygame.event import Event

import game_settings
from collisions import check_collision, check_wall_collision
from enemy import Enemy
from game_settings import *
from player import Player


def get_starting_positions(number):
    positions = []
    map_positions = list(TANK_POSSIBLE_POSITIONS)
    for _ in range(number):
        el = random.choice(map_positions)
        positions.append(el)
        map_positions.remove(el)
    return positions


def set_map():
    return pygame.image.load('maps/map0{0}.jpg'.format(str(random.randint(1, NUMBER_OF_MAP))))


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

        positions = get_starting_positions(NUMBER_OF_ENEMIES + 1)
        self.player = Player(CONTROL_TANK, positions[0][0], positions[0][1], MOVEMENT_SPEED, ROTATION_SPEED)
        self.enemies = [Enemy(positions[i][0], positions[i][1], MOVEMENT_SPEED, ROTATION_SPEED)
                        for i in range(1, NUMBER_OF_ENEMIES + 1)]
        self.tanks = []

        self.game_state = GameState.GAME_ON

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
            shells += tank.shells

        for shell in shells:
            shell.move(SHELL_SPEED)
            for point in shell.points.values():
                if check_wall_collision(point):
                    for shooting_tank in self.tanks:
                        shooting_tank.pop_shell(shell)

            for tank in self.tanks:
                if check_collision(shell, tank) and tank.alive:
                    tank.destroy()
                    for shooting_tank in self.tanks:
                        shooting_tank.pop_shell(shell)

    def draw(self):
        self.screen.blit(MAP, (0, 0))
        for tank in self.tanks:
            tank.draw(self.screen)
            for shell in tank.shells:
                shell.draw(self.screen)
            tank.check_shells()
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
        game_settings.MAP = set_map()
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
