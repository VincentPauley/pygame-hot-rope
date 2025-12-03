import math
import os

import pygame

from classes.button import Button
from classes.easement import Easement
from classes.player import Player, PlayerParams
from colors import COLOR_PRIMARY_BLUE
from config import game_config

# time to code split and cleanup:

# [ ] - player should be it's own class
# [ ] - fireballs should be separate functions and be stored in a loop.
# [ ] - move fireball image to asset folder

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]

script_dir = os.path.dirname(__file__)

image_filename = "fireball.png"

monster_image_path = os.path.join("src", "assets", "hot-rope-monster.png")

image_path = os.path.join(script_dir, image_filename)


starting_rope_angle = 25


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

    current_angle = starting_rope_angle
    angular_velocity = 0.11

    outermost_fireball_pos = rope_circle_radius - 70

    game_over = False

    player_class_instance = Player(PlayerParams(coordinates=(250, SCREEN_HEIGHT - 150)))

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

        self.monster_image = pygame.image.load(monster_image_path).convert_alpha()

        self.scaled_monster_image = pygame.transform.scale(
            self.monster_image, (140, 200)
        )

        self.monster_rect = self.scaled_monster_image.get_rect(
            center=(SCREEN_WIDTH // 2, 240)
        )

        self.monster_velocity = 1

        self.rope_active = False

        self.start_message = font.render("Click 'Space' to Play.", True, "black")
        self.start_message_rect = self.start_message.get_rect(
            center=(SCREEN_WIDTH // 2, 50)
        )

        self.game_over_message = font.render("Game Over!", True, "black")
        self.game_over_rect = self.game_over_message.get_rect(
            center=(SCREEN_WIDTH // 2, 50)
        )

        self.monster_easement = Easement(380, 420, 0.5)

    def reset(self):
        print("class Level: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.current_angle = starting_rope_angle

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()

    def receive_jump_input(self):
        self.rope_active = True
        # note: no double jumps for now
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -20

    def receive_player_input(self, input_type: str):
        if input_type == "space":
            self.player_class_instance.receive_jump_input()

    # NOTE: does this need to be done for each fireball? might be able to just
    # do once for outer and then calc dist between those 2 points for other centers
    def calc_fireball_pos(self, center_offset, sin_angle, cos_angle):
        dist_from_center = self.outermost_fireball_pos * center_offset

        return [
            round(self.rope_circle_pos[0] + dist_from_center * sin_angle),
            round(self.rope_circle_pos[1] + dist_from_center * cos_angle),
        ]

    # step one: detect input and change color.
    def run(self, delta_time):
        self.main_menu_button.check_for_click()
        self.screen.fill("navajowhite2")
        self.main_menu_button.draw(self.screen)

        if self.rope_active:
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

        if (
            fireball_rect.colliderect(self.player_class_instance.rect)
            and self.player_class_instance.jump_height < 100
        ):
            self.player_class_instance.killed = True
            self.game_over = True
            self.rope_active = False

        self.monster_easement.update(delta_time)
        self.monster_rect.centerx = round(self.monster_easement.current_position)

        self.screen.blit(self.scaled_monster_image, self.monster_rect)

        if self.game_over:
            self.screen.blit(self.game_over_message, self.game_over_rect)
            # Note: Still not able to change speed from the easment class
        elif not self.rope_active:
            self.screen.blit(self.start_message, self.start_message_rect)

        self.player_class_instance.update(delta_time)
        self.player_class_instance.draw(self.screen)

        # up next: "Click Space to start & Reset"
        # fling player
        # have player remove themselves from class when killed
        # score keeping
        # varying speed of rope (do it with rotation count, not time)
