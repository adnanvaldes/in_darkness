import pygame

# GLOBAL VARIABLES

WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
PLAYER_SPEED = 5
ROBOT_SPEED = 4
MAX_ROBOTS = 5
MAX_COINS = 10
MAX_DOORS = 1
# First number is boost period in seconds; second one is to convert to miliseconds to patch Pygame's clock
BOOST_PERIOD = (10) * 1000
SCORE_FONT = ("Arial", 24)
SCORE_DIFFICULTY_INCREASE = True

# Player controls
MOVEMENT_KEYS = {
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_a: "left",
    pygame.K_d: "right",
    pygame.K_w: "up",
    pygame.K_s: "down",
}
