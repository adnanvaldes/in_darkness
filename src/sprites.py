import pygame


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
    width = sprite.get_width()
    height = sprite.get_height()


class Coin(Sprite):
    """
    Class to implement coins
    """

    sprite = pygame.image.load("src/coin.png")
    width = sprite.get_width()
    height = sprite.get_height()


class Door(Sprite):
    """
    Class to implement doors
    """

    sprite = pygame.image.load("src/door.png")
    width = sprite.get_width()
    height = sprite.get_height()
