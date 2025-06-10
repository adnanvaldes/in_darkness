import pygame
import random

from sprites import Monster, Robot, Door, Coin

WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)


class InDarkness:
    """
    Main class for the game. Contains all functionality
    to play the game and keeps track of the current game state
    """

    def __init__(self):
        pygame.init()

        # Window variables
        self.width = WIDTH
        self.height = HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("In Darkness")
        pygame.display.set_icon(Monster.sprite)

        # Game variables
        self.clock = pygame.time.Clock()
        self.monster = Monster(self.width - Monster.width, self.height - Monster.height)
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
            self.draw_window()
            self.clock.tick()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def draw_window(self):
        self.window.fill(BLACK)
        self.monster.render(self.window)
        pygame.display.flip()


if __name__ == "__main__":
    InDarkness()
