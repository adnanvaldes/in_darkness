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
MAX_COINS = 5
MAX_DOORS = 1

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
