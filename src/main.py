import pygame
import random

WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)


class Sprite:
    """
    Superclass to implement common functionality

    Note that the sprite PNG itself is loaded by the specific class to avoid
    reloading the image every time a new instance is created
    """

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def update(self):
        pass

    def render(self, window):
        window.blit(self.sprite, (self.x, self.y))


class Monster(Sprite):
    """
    Class to implement the main character
    """

    sprite = pygame.image.load("src/monster.png")
    width = sprite.get_width()
    height = sprite.get_height()


class Robot(Sprite):
    """
    Class to implement enemies
    """

    sprite = pygame.image.load("src/robot.png")


class Objects(Sprite):
    """
    Class to implement objects, which the Monster can interact with
    These can be either coins or doors.
    """

    coin_sprite = pygame.image.load("src/coin.png")
    door_sprite = pygame.image.load("src/door.png")


class InDarkness:
    """
    Main class for the game. Contains all functionality
    to play the game and keeps track of the current game state
    """

    def __init__(self):
        pygame.init()

        self.width = WIDTH
        self.height = HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("In Darkness")
        pygame.display.set_icon(Monster.sprite)

        self.monster = Monster()

        self.main_loop()

    def main_loop(self):
        """
        Main loop of the game
        """
        while True:
            self.check_events()
            self.draw_window()

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
