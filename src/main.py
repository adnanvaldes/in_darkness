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

        self.instructions()
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
        """
        Initializes the game state. Also used when resetting the game.
        """
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
        self.paused = False

        # Sprite variables
        self.monster = Monster()
        self.robots = [Robot() for robot in range(config.MAX_ROBOTS)]
        self.coins = [Coin() for coin in range(config.MAX_COINS)]
        self.doors = [Door() for door in range(config.MAX_DOORS)]
        self.sprites = [self.robots, self.coins, self.doors]

    def instructions(self):
        """
        Print game instructions
        """
        title_font = pygame.font.SysFont("Arial", 48)
        instruction_font = pygame.font.SysFont("Arial", 24)
        small_font = pygame.font.SysFont("Arial", 18)

        waiting_for_key = True
        clock = pygame.time.Clock()

        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    else:
                        waiting_for_key = False

            self.window.fill(config.BLACK)

            title_surface = title_font.render("IN DARKNESS", True, config.RED)
            title_rect = title_surface.get_rect(center=(self.width // 2, 70))
            self.window.blit(title_surface, title_rect)

            instructions = [
                "HOW TO PLAY:",
                "",
                "MOVEMENT:",
                "Arrow Keys or WASD - Move your character",
                "",
                "OBJECTIVE:",
                "Collect all coins while avoiding robots",
                "",
                "POWER-UPS:",
                "Blue squares (Doors) - Boost your speed temporarily",
                "",
                "CONTROLS:",
                "SPACE - Restart game",
                "ESC - Quit game",
                "P - See instructions/pause" "",
                "",
                "Source code at https://github.com/adnanvaldes/in_darkness",
                "Press any key to start...",
            ]

            y_offset = 140
            line_spacing = 25

            for line in instructions:
                if line == "HOW TO PLAY:" or line == "Press any key to start...":
                    # Large font for header
                    surface = instruction_font.render(line, True, config.RED)
                elif line in ["MOVEMENT:", "OBJECTIVE:", "POWER-UPS:", "CONTROLS:"]:
                    # Use medium font for sections
                    surface = instruction_font.render(line, True, config.YELLOW)
                elif line == "":
                    # Skip empty lines but maintain spacing
                    y_offset += line_spacing
                    continue  # Without continue text overflows screen
                else:
                    # Small font for details
                    surface = small_font.render(line, True, config.GRAY)

                rect = surface.get_rect(center=(self.width // 2, y_offset))
                self.window.blit(surface, rect)
                y_offset += line_spacing

            pygame.display.flip()
        clock.tick(30)

    def pause(self):
        """
        Stop main loop from running and show instructions agian.
        This method also keeps track of how long the game was paused
        so that pauses don't affect play time
        """
        self.paused = True
        pause_start_time = pygame.time.get_ticks()

        self.instructions()

        pause_duration = pygame.time.get_ticks() - pause_start_time
        self.start_time += pause_duration

        self.paused = False

    def check_events(self):
        """
        Handle keyboard inputs
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    self.initialize()
                if event.key == pygame.K_p:
                    self.pause()
            self.monster.move(event)

    def update_sprites(self):
        """
        Update position of all sprites in the game and check for colissions
        """
        if not self.paused:
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
            self.handle_robot_collisions()

    def add_robot(self):
        max_robots = (
            max(config.MAX_ROBOTS, int(self.score / 2))
            if config.SCORE_DIFFICULTY_INCREASE
            else config.MAX_ROBOTS
        )

        if len(self.robots) < max_robots and self.robot_timer >= self.robot_next_spawn:
            self.robots.append(Robot())
            self.robot_next_spawn = random.randint(30, 120)
            self.robot_timer = 0

    def add_coin(self):
        max_coins = 10000 if self.game_over else config.MAX_COINS

        if len(self.coins) < max_coins and self.coin_timer >= self.coin_next_spawn:
            self.coins.append(Coin())
            self.coin_next_spawn = random.randint(60, 120)
            self.coin_timer = 0

    def handle_robot_collisions(self):
        total_robots = len(self.robots)
        for i in range(total_robots):
            for j in range(i + 1, total_robots):
                robot1 = self.robots[i]
                robot2 = self.robots[j]

                if robot1.get_rect().colliderect(robot2.get_rect()):
                    robot1.speed *= -1
                    robot2.speed *= -1

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
        # Draw rectangle over monster eyes for testing
        # pygame.draw.rect(self.window, config.RED, self.monster.get_collision_rect(), 1)

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


if __name__ == "__main__":
    InDarkness()
