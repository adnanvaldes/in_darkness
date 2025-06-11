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
        self.font = pygame.font.SysFont(*config.SCORE_FONT)

        # Game variables
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.robot_next_spawn = random.randint(0, 120)
        self.coin_next_spawn = random.randint(60, 180)
        self.robot_timer = 0
        self.coin_timer = 0
        self.door_timer = 0
        self.touched_door = False
        self.score = 0
        self.game_over = False

        # Sprite variables
        self.monster = Monster()
        self.robots = [Robot() for robot in range(config.MAX_ROBOTS)]
        self.coins = [Coin() for coin in range(config.MAX_COINS)]
        self.doors = [Door() for door in range(config.MAX_DOORS)]
        self.sprites = [self.robots, self.coins, self.doors]

        self.main_loop()

    def main_loop(self):
        """
        Main loop of the game
        """
        while True:
            self.robot_timer += 1
            self.coin_timer += 1
            self.door_timer += 1
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

        score = self.font.render(f"Score: {self.score}", True, (255, 0, 0))
        if not self.game_over:
            self.monster.render(self.window)
            self.window.blit(score, (config.WIDTH - 100, 25))
        else:
            score_rect = score.get_rect(
                center=(config.WIDTH // 2, config.HEIGHT // 2 + 30)
            )
            self.window.blit(score, score_rect)
            self.font = pygame.font.SysFont(
                config.SCORE_FONT[0], config.SCORE_FONT[1] * 2
            )
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(
                center=(config.WIDTH // 2, config.HEIGHT // 2 - 20)
            )
            self.window.blit(game_over_text, game_over_rect)

        for sprite_type in self.sprites:
            for entity in sprite_type:
                entity.render(self.window)
        pygame.display.flip()

    def add_robot(self):
        if (
            len(self.robots) < config.MAX_ROBOTS
            and self.robot_timer >= self.robot_next_spawn
        ):
            self.robots.append(Robot())
            self.robot_robot_next_spawn = random.randint(30, 120)
            self.robot_timer = 0

    def add_coin(self):
        if (
            len(self.coins) < config.MAX_COINS
            and self.coin_timer >= self.coin_next_spawn
        ):
            self.coins.append(Coin())
            self.coin_next_spawn = random.randint(60, 120)
            self.coin_timer = 0

    def update_sprites(self):
        # add entities
        self.add_robot()
        self.add_coin()

        # Update entities
        self.monster.update()

        # Check if boosted speed needs to be reset
        if (
            self.door_timer > 0
            and pygame.time.get_ticks() - self.door_timer >= config.BOOST_PERIOD
            and self.touched_door
        ):
            self.monster.speed = config.PLAYER_SPEED
            self.touched_door = False
            self.door_timer = 0

        for sprite_type in self.sprites:
            for entity in sprite_type:
                entity.update()
                if entity.get_rect().colliderect(self.monster.get_rect()):
                    if isinstance(entity, Coin):
                        self.coins.remove(entity)
                        self.score += 1
                    if isinstance(entity, Robot):
                        self.game_over = True
                    if isinstance(entity, Door) and self.touched_door == False:
                        self.touched_door = True
                        self.door_timer = pygame.time.get_ticks()
                        self.monster.speed *= 1.5


if __name__ == "__main__":
    InDarkness()
