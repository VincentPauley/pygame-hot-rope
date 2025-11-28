import pygame

from classes.button import Button
from colors import COLOR_PRIMARY_BLUE
from config import game_config

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]


class Level:
    velocity = 0
    gravity = 1
    is_jumping = False
    jump_color = "royalblue1"

    player_width = 50
    player_height = 50

    player_spot_x = 250
    palyer_spot_y = SCREEN_HEIGHT - 150

    rope_circle_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    rope_circle_radius = 275

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.game_state_manager = game_state_manager
        self.main_menu_button = Button(
            "Main Menu",
            lambda: game_state_manager.set_state("main_menu"),
            COLOR_PRIMARY_BLUE,
            (10, 10),
            (150, 50),
        )
        self.player_color = "royalblue"
        self.player = pygame.Rect(
            self.player_spot_x,
            self.palyer_spot_y,
            self.player_width,
            self.player_height,
        )

        print("SCREEN_HEIGHT: ", SCREEN_HEIGHT / 2)
        print("SCREEN_WIDTH: ", SCREEN_WIDTH / 2)

    def reset(self):
        print("class Level: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()

    def receive_jump_input(self):
        # note: no double jumps for now
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -20

    def calc_shadow(self):
        shadow = pygame.Rect(
            self.player_spot_x,
            self.palyer_spot_y + (self.player_height / 2),
            self.player_width * (SCREEN_HEIGHT - self.player.y) / 140,
            self.player_height * 0.8,
        )

        shadow.centerx = self.player.centerx

        return shadow

    # step one: detect input and change color.
    def run(self, delta_time):
        self.main_menu_button.check_for_click()
        self.screen.fill("gold")
        self.main_menu_button.draw(self.screen)
        # pygame.draw.rect(self.screen, self.player_color, self.player)

        player_circle_center = self.player.center
        player_circle_radius = min(self.player.width, self.player.height) // 2

        # apply gravity to velo
        if self.is_jumping:
            self.velocity = self.velocity + self.gravity
            self.player.y += self.velocity * delta_time * 60
            if self.player.y >= self.palyer_spot_y:
                self.player.y = self.palyer_spot_y
                self.is_jumping = False
                self.velocity = 0

        # draw player spot
        # pygame.draw.rect(
        #     self.screen,
        #     "white",
        #     (
        #         self.player_spot_x,
        #         self.palyer_spot_y,
        #         self.player_width,
        #         self.player_height,
        #     ),
        # )

        pygame.draw.circle(
            self.screen, "yellow", self.rope_circle_pos, self.rope_circle_radius
        )

        shadow_rect = self.calc_shadow()

        # drwa shadow
        # pygame.draw.rect(self.screen, "red", shadow_rect)

        pygame.draw.ellipse(self.screen, "orange", shadow_rect)

        current_color = self.jump_color if self.is_jumping else self.player_color

        pygame.draw.circle(
            self.screen, current_color, player_circle_center, player_circle_radius
        )
