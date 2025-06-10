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
        self.monster = Monster(
            self.width / 2 - Monster.width, self.height / 2 - Monster.height
        )
        self.coins = []
        self.robots = []
        self.doors = []

        self.main_loop()

    def main_loop(self):
        """
        Main loop of the game
        """
        while True:
            self.check_events()
            self.monster.update()
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
        pygame.display.flip()


if __name__ == "__main__":
    InDarkness()
