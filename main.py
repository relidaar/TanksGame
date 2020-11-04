from pygame.event import Event

import game_settings
from collisions import check_wall_collision, check_collision
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


def reset_map():
    return pygame.image.load('maps/map0{0}.jpg'.format(str(random.randint(1, NUMBER_OF_MAP))))


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        positions = get_starting_positions(2)
        self.player = Player(positions[0][0], positions[0][1], 0, CONTROL_TANK)
        self.tank_list = []

    def process(self, event: Event):
        if event.type == pygame.QUIT:
            self.running = False
        self.player.shoot_control(event)

    def update(self):
        if not self.player.alive:
            for tank in self.tank_list:
                if tank.alive:
                    tank.score += 1
                tank.alive = True
            self.run()
            return

        self.player.move_control()
        ball_list = []
        for tank in self.tank_list:
            ball_list += tank.shells

        for shell in ball_list:
            shell.move(SHELL_SPEED)
            for point in shell.points.values():
                if check_wall_collision(point):
                    for shooting_tank in self.tank_list:
                        shooting_tank.pop_shell(shell)

            for tank in self.tank_list:
                if check_collision(shell, tank) and tank.alive:
                    tank.alive = False
                    tank.destroy()
                    for shooting_tank in self.tank_list:
                        shooting_tank.pop_shell(shell)

    def draw(self):
        self.screen.blit(MAP, (0, 0))
        for tank in self.tank_list:
            tank.draw(self.screen)
            for shell in tank.shells:
                shell.draw(self.screen)
            tank.check_shells()
        self.draw_score(str(self.player.score))
        pygame.display.update()

    def draw_text(self, text, color, size, location):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = location
        self.screen.blit(text_surface, text_rect)

    def draw_score(self, score):
        self.draw_text(score, BLACK, 60, (30, 10))

    def run(self):
        game_settings.MAP = reset_map()
        positions = get_starting_positions(3)
        self.player.change_location(positions[0][0], positions[0][1])
        self.tank_list = [self.player]

        for tank in self.tank_list:
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
