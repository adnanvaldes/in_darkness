import pygame
import math
import config


def load_scaled(path, scale=0.5):
    image = pygame.image.load(path)
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))


class Sprite:
    """
    Superclass to implement common functionality

    Note that the sprite PNG itself is loaded by the specific class to avoid
    reloading the image every time a new instance is created
    """

    width = 0
    height = 0

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def render(self, window):
        window.blit(self.sprite, (self.x, self.y))

    def x_on_screen(self, new_x):
        return max(0, min(new_x, config.WIDTH - type(self).width))

    def y_on_screen(self, new_y):
        return max(0, min(new_y, config.HEIGHT - type(self).height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, type(self).width, type(self).height)


class Monster(Sprite):
    """
    Class to implement the main character
    """

    sprite = load_scaled("src/monster.png")
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = config.PLAYER_SPEED
        self.movement = MOVEMENT_KEYS
        self.left = False
        self.right = False
        self.down = False
        self.up = False

    def move(self, event):
        match event.type:
            case pygame.KEYDOWN:
                if event.key in self.movement:
                    # This allows to translate the dict value to an attribute of that name in this object
                    setattr(self, self.movement[event.key], True)
            case pygame.KEYUP:
                if event.key in self.movement:
                    setattr(self, self.movement[event.key], False)

    def update(self):
        dx = 0
        dy = 0

        if self.left:
            dx -= 1
        if self.right:
            dx += 1
        if self.up:
            dy -= 1
        if self.down:
            dy += 1

        # Normalize if moving diagonally
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx = dx / length
            dy = dy / length

            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed

            self.x = self.x_on_screen(new_x)
            self.y = self.y_on_screen(new_y)


class Robot(Sprite):
    """
    Class to implement enemies
    """

    sprite = load_scaled("src/robot.png")
    width = sprite.get_width()
    height = sprite.get_height()


class Coin(Sprite):
    """
    Class to implement coins
    """

    sprite = load_scaled("src/coin.png")
    width = sprite.get_width()
    height = sprite.get_height()


class Door(Sprite):
    """
    Class to implement doors
    """

    sprite = load_scaled("src/door.png")
    width = sprite.get_width()
    height = sprite.get_height()
