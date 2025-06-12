import pygame
import math
import random

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

    def __init__(self):
        self.x = random.randint(0, config.WIDTH - self.width)
        self.y = random.randint(0, config.HEIGHT - self.height)

    def render(self, window):
        window.blit(self.sprite, (self.x, self.y))

    def update(self):
        pass

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

    sprite = load_scaled("monster.png", config.PLAYER_SCALE)
    scaled_sprite = load_scaled("monster.png")
    width, height = scaled_sprite.get_size()

    # Numbers found experimentally by drawing a rectangle in game over the monster. It will not work if the scale is modified.
    EYES_OFFSET_X = 18
    EYES_OFFSET_Y = 15
    EYES_WIDTH = 18
    EYES_HEIGHT = 7
    OFFSET_X = EYES_OFFSET_X * config.PLAYER_SCALE
    OFFSET_Y = EYES_OFFSET_Y * config.PLAYER_SCALE
    SCALED_EYES_WIDTH = EYES_WIDTH * config.PLAYER_SCALE
    SCALED_EYES_HEIGHT = EYES_HEIGHT * config.PLAYER_SCALE

    def __init__(self):
        self.x = config.WIDTH / 2 - Monster.width
        self.y = config.HEIGHT / 2 - Monster.height
        self.speed = config.PLAYER_SPEED
        self.movement = config.MOVEMENT_KEYS
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

    def x_on_screen(self, new_x):
        new_width = self.OFFSET_X + self.SCALED_EYES_WIDTH
        return max(-self.OFFSET_X, min(new_x, config.WIDTH - new_width))

    def y_on_screen(self, new_y):
        new_height = self.OFFSET_Y + self.SCALED_EYES_HEIGHT
        return max(-self.OFFSET_Y, min(new_y, config.HEIGHT - new_height))

    def get_rect(self):
        collision_x = self.x + self.OFFSET_X
        collision_y = self.y + self.OFFSET_Y

        return pygame.Rect(
            collision_x,
            collision_y,
            self.SCALED_EYES_WIDTH,
            self.SCALED_EYES_HEIGHT,
        )


class Robot(Sprite):
    """
    Class to implement enemies
    """

    sprite = load_scaled("robot.png")
    width, height = sprite.get_size()

    def __init__(self):
        self.speed = config.ROBOT_SPEED
        self.patrol = random.choice(["x_axis", "y_axis"])

        edge = random.choice(["top", "bottom", "left", "right"])

        if edge == "top":
            self.x = random.randint(0, config.WIDTH - self.width)
            self.y = 0
        elif edge == "bottom":
            self.x = random.randint(0, config.WIDTH - self.width)
            self.y = config.HEIGHT - self.height
        elif edge == "left":
            self.x = 0
            self.y = random.randint(0, config.HEIGHT - self.height)
        elif edge == "right":
            self.x = config.WIDTH - self.width
            self.y = random.randint(0, config.HEIGHT - self.height)

    def update(self):
        if self.patrol == "x_axis":
            new_x = self.x + self.speed
            if new_x <= 0 or new_x >= config.WIDTH - self.width:
                self.speed *= -1
            self.x = self.x_on_screen(self.x + self.speed)
        else:
            new_y = self.y + self.speed
            if new_y <= 0 or new_y >= config.HEIGHT - self.height:
                self.speed *= -1
            self.y = self.y_on_screen(self.y + self.speed)


class Coin(Sprite):
    """
    Class to implement coins
    """

    sprite = load_scaled("coin.png")
    width, height = sprite.get_size()


class Door(Sprite):
    """
    Class to implement doors
    """

    sprite = load_scaled("door.png")
    width, height = sprite.get_size()
