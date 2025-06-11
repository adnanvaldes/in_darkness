import pygame
import random

from sprites import Monster, Robot, Door, Coin
import config


class InDarkness:
    """
    Main class for the game. Contains all functionality
    to play the game and keeps track of the current game state
    """

    def __init__(self):
        pygame.init()

        # Window variables
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("In Darkness")
        pygame.display.set_icon(Monster.sprite)

        # Game variables
        self.clock = pygame.time.Clock()
        self.next_spawn = random.randint(0, 120)
        self.timer = 0
        self.score = 0

        # Sprite variables
        self.monster = Monster()
        self.robots = [Robot() for robot in range(config.MAX_ROBOTS + 1)]
        self.coins = [Coin() for coin in range(config.MAX_COINS + 1)]
        self.doors = [Door() for door in range(config.MAX_DOORS + 1)]
        self.sprites = [self.robots, self.coins, self.doors]

        self.main_loop()

    def main_loop(self):
        """
        Main loop of the game
        """
        while True:
            self.timer += 1
            self.check_events()
            self.update_sprites()
            self.draw_window()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            self.monster.move(event)

    def draw_window(self):
        self.window.fill(config.BLACK)
        self.monster.render(self.window)
        for sprite_type in self.sprites:
            for entity in sprite_type:
                entity.render(self.window)
        pygame.display.flip()

    def add_robot(self):
        if len(self.robots) < config.MAX_ROBOTS and self.timer >= self.next_spawn:
            self.robots.append(Robot())
            self.reset_spawn_timer()

    def reset_spawn_timer(self):
        self.next_spawn = random.randint(30, 120)
        self.timer = 0

    def update_sprites(self):
        # add entities
        self.add_robot()

        # Update entities
        self.monster.update()
        for sprite_type in self.sprites:
            for entity in sprite_type:
                entity.update()


if __name__ == "__main__":
    InDarkness()
