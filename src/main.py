import pygame

WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)


class Monster:
    """
    Class to implement the main character
    """

    sprite = pygame.image.load("src/monster.png")

    pass


class Robot:
    """
    Class to implement enemies
    """

    sprite = pygame.image.load("src/robot.png")
    pass


class Objects:
    """
    Class to implement objects, which the Monster can interact with
    These can be either coins or doors.
    """

    coin_sprite = pygame.image.load("src/coin.png")
    door_sprite = pygame.image.load("src/door.png")

    pass


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


if __name__ == "__main__":
    InDarkness()
