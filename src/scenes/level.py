import math
import os

import pygame

from classes.button import Button
from colors import COLOR_PRIMARY_BLUE
from config import game_config

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]

script_dir = os.path.dirname(__file__)

image_filename = "fireball.png"


# fireball_surf = pygame.image.load("./fireball.png")

image_path = os.path.join(script_dir, image_filename)


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

    current_angle = 0
    angular_velocity = 0.05

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

        self.fireball_image = pygame.image.load(image_path).convert_alpha()

        self.fireball_rect = self.fireball_image.get_rect(center=(100, 100))

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
        self.screen.fill("navajowhite2")
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

        shadow_rect = self.calc_shadow()

        # drwa shadow
        # pygame.draw.rect(self.screen, "red", shadow_rect)

        pygame.draw.ellipse(self.screen, "orange", shadow_rect)

        self.current_angle += self.angular_velocity * delta_time * 60
        # Keep angle within 0 to 2*pi
        self.current_angle %= 2 * math.pi

        starting_outer = self.rope_circle_radius - 70

        death_ball_x = self.rope_circle_pos[0] + starting_outer * math.cos(
            self.current_angle
        )

        death_ball_y = self.rope_circle_pos[1] + starting_outer * math.sin(
            self.current_angle
        )

        death_ball_2_x = self.rope_circle_pos[0] + (starting_outer * 0.75) * math.cos(
            self.current_angle
        )

        death_ball_2_y = self.rope_circle_pos[1] + (starting_outer * 0.75) * math.sin(
            self.current_angle
        )

        death_ball_3_x = self.rope_circle_pos[0] + (starting_outer * 0.5) * math.cos(
            self.current_angle
        )

        death_ball_3_y = self.rope_circle_pos[1] + (starting_outer * 0.5) * math.sin(
            self.current_angle
        )

        death_ball_4_x = self.rope_circle_pos[0] + (starting_outer * 0.25) * math.cos(
            self.current_angle
        )

        death_ball_4_y = self.rope_circle_pos[1] + (starting_outer * 0.25) * math.sin(
            self.current_angle
        )

        pygame.draw.circle(
            self.screen,
            "yellow",
            (death_ball_2_x, death_ball_2_y),
            player_circle_radius,
        )
        pygame.draw.circle(
            self.screen,
            "yellow",
            (death_ball_3_x, death_ball_3_y),
            player_circle_radius,
        )
        pygame.draw.circle(
            self.screen,
            "yellow",
            (death_ball_4_x, death_ball_4_y),
            player_circle_radius,
        )

        ball_placement = pygame.Rect(0, 0, 50, 50)

        ball_placement.center = (death_ball_x, death_ball_y)

        something = self.fireball_image.get_rect(center=(death_ball_x, death_ball_y))

        current_color = self.jump_color if self.is_jumping else self.player_color

        pygame.draw.circle(
            self.screen, current_color, player_circle_center, player_circle_radius
        )

        self.screen.blit(self.fireball_image, something)
