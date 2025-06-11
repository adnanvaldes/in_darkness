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

        self.initialize()
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

    def initialize(self):
        # Game variables
        self.font = pygame.font.SysFont(*config.SCORE_FONT)
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
        self.collected_all_coins = False

        # Sprite variables
        self.monster = Monster()
        self.robots = [Robot() for robot in range(config.MAX_ROBOTS)]
        self.coins = [Coin() for coin in range(config.MAX_COINS)]
        self.doors = [Door() for door in range(config.MAX_DOORS)]
        self.sprites = [self.robots, self.coins, self.doors]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    self.initialize()
            self.monster.move(event)

    def draw_window(self):
        self.window.fill(config.BLACK)

        if not self.game_over:
            self._draw_game_screen()
        else:
            self._draw_game_over_screen()

        # Draw all sprites
        for sprite_type in self.sprites:
            for entity in sprite_type:
                entity.render(self.window)

        pygame.display.flip()

    def _draw_game_screen(self):
        self.monster.render(self.window)
        score_text = self.font.render(f"Score: {self.score}", True, config.RED)
        self.window.blit(score_text, (config.WIDTH - 100, 25))

    def _draw_game_over_screen(self):
        # Define fonts
        score_font = pygame.font.SysFont(
            config.SCORE_FONT[0], int(config.SCORE_FONT[1])
        )
        time_font = pygame.font.SysFont(config.SCORE_FONT[0], int(config.SCORE_FONT[1]))
        title_font = pygame.font.SysFont(config.SCORE_FONT[0], config.SCORE_FONT[1] * 2)

        # Define text surfaces
        game_over_text = "YOU WON" if self.collected_all_coins else "GAME OVER"
        title_surface = title_font.render(game_over_text, True, config.RED)
        score_surface = score_font.render(f"Score: {self.score}", True, config.RED)
        time_surface = time_font.render(
            f"Time: {self.game_duration()}", True, config.RED
        )

        # Draw text
        title_rect = title_surface.get_rect(center=self.align_text(1))
        time_rect = time_surface.get_rect(center=self.align_text(2))
        score_rect = score_surface.get_rect(center=self.align_text(3))

        self.window.blit(title_surface, title_rect)
        self.window.blit(score_surface, score_rect)
        self.window.blit(time_surface, time_rect)

    def align_text(self, line_number, lines=3, spacing=40):
        center_x = config.WIDTH // 2
        total_height = (lines - 1) * spacing
        start_y = (config.HEIGHT // 2) - (total_height / 2)
        y = start_y + (line_number * spacing)
        return (center_x, y)

    def game_duration(self):
        milliseconds = self.current_time - self.start_time
        total_seconds = milliseconds // 1000

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        minutes_text = "minutes"
        if minutes == 1:
            minutes_text = "minute"

        seconds_text = "seconds"
        if seconds == 1:
            seconds_text = "second"

        if minutes > 0:
            return f"{minutes} {minutes_text} {seconds} {seconds_text}"
        else:
            return f"{seconds} {seconds_text}"

    def add_robot(self):
        # Increase difficulty if score is 30
        if config.SCORE_DIFFICULTY_INCREASE:
            config.MAX_ROBOTS = max(config.MAX_ROBOTS, int(self.score / 2))
        if (
            len(self.robots) < config.MAX_ROBOTS
            and self.robot_timer >= self.robot_next_spawn
        ):
            self.robots.append(Robot())
            self.robot_next_spawn = random.randint(30, 120)
            self.robot_timer = 0

    def add_coin(self):
        if self.game_over:
            config.MAX_COINS = 10000

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
        if not self.game_over:
            self.monster.update()
            self.current_time = pygame.time.get_ticks()
        else:
            # Place player outside of screen
            self.monster.x = 500
            self.monster.y = 500

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
                if len(self.coins) == 0:
                    self.collected_all_coins = True
                    self.game_over = True
                    break
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
