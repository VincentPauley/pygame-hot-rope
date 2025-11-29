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
    dead_color = "darkred"

    player_width = 50
    player_height = 50

    player_spot_x = 250
    palyer_spot_y = SCREEN_HEIGHT - 150

    rope_circle_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    rope_circle_radius = 275

    current_angle = 0
    angular_velocity = 0.05

    outermost_fireball_pos = rope_circle_radius - 70

    player_killed = False

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

    # NOTE: does this need to be done for each fireball? might be able to just
    # do once for outer and then calc dist between those 2 points for other centers
    def calc_fireball_pos(self, center_offset, sin_angle, cos_angle):
        dist_from_center = self.outermost_fireball_pos * center_offset

        return [
            round(self.rope_circle_pos[0] + dist_from_center * sin_angle),
            round(self.rope_circle_pos[1] + dist_from_center * cos_angle),
        ]

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

        pygame.draw.ellipse(self.screen, "orange", shadow_rect)

        self.current_angle += self.angular_velocity * delta_time * 60
        # Keep angle within 0 to 2*pi
        self.current_angle %= 2 * math.pi

        cos_angle = math.cos(self.current_angle)
        sin_angle = math.sin(self.current_angle)

        death_ball_1 = self.calc_fireball_pos(1, cos_angle, sin_angle)
        death_ball_2 = self.calc_fireball_pos(0.75, cos_angle, sin_angle)
        death_ball_3 = self.calc_fireball_pos(0.5, cos_angle, sin_angle)
        death_ball_4 = self.calc_fireball_pos(0.25, cos_angle, sin_angle)

        fireball_rect = self.fireball_image.get_rect(center=(death_ball_1))
        fireball_rect_2 = self.fireball_image.get_rect(center=(death_ball_2))
        fireball_rect_3 = self.fireball_image.get_rect(center=(death_ball_3))
        fireball_rect_4 = self.fireball_image.get_rect(center=(death_ball_4))

        # fireball_rect

        self.screen.blit(self.fireball_image, fireball_rect)
        self.screen.blit(self.fireball_image, fireball_rect_2)
        self.screen.blit(self.fireball_image, fireball_rect_3)
        self.screen.blit(self.fireball_image, fireball_rect_4)

        current_color = self.dead_color if self.player_killed else self.player_color

        # draw player to screen
        pygame.draw.circle(
            self.screen, current_color, player_circle_center, player_circle_radius
        )
        # draw collision points for fields
        player_hit_box = pygame.Rect(0, 0, self.player.width, self.player.height)

        player_hit_box.center = player_circle_center

        # this rect is the collision point between the player and fireball
        pygame.draw.rect(self.screen, "red", fireball_rect, 2)
        pygame.draw.rect(self.screen, "blue", player_hit_box, 2)

        if fireball_rect.colliderect(player_hit_box) and not self.is_jumping:
            self.player_killed = True
