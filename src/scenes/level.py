import math
import os
import random

import pygame

from classes.easement import Easement
from classes.end_game_menu import EndGameMenu
from classes.fireball import (
    Fireball,
    FireballParams,
    FireballPosParams,
    FireballUpdateParams,
)
from classes.player import Player, PlayerParams
from config import game_config

# time to code split and cleanup:

# [ ] - fireballs should be separate functions and be stored in a loop.
# [ ] - move fireball image to asset folder
# might want to have all of the things in a scene as an array so you can just
# loop through and update/draw the active ones and not worry about others... array
# also might allow for straight up removal.

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]

script_dir = os.path.dirname(__file__)

image_filename = "fireball.png"

monster_image_path = os.path.join("src", "assets", "hot-rope-monster.png")
bg_image_path = os.path.join("src", "assets", "beach-bg.png")

image_path = os.path.join(script_dir, image_filename)


starting_rope_angle = 25

rope_speeds = {
    "slow": 0.08,
    "medium": 0.13,
    "fast": 0.18,
}


class Level:
    rope_circle_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    rope_circle_radius = 275

    current_angle = starting_rope_angle
    angular_velocity = rope_speeds["medium"]
    active_rope_speed = "medium"

    outermost_fireball_pos = rope_circle_radius - 70

    game_over = False

    rope_passing_started = False

    last_speed_change_rotation = 0
    rotations_completed = 0

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.game_state_manager = game_state_manager
        self.end_game_menu = EndGameMenu(self.handle_main_menu_click, self.reset)

        self.fireball_image = pygame.image.load(image_path).convert_alpha()

        self.bg_image = pygame.image.load(bg_image_path).convert()

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

        self.fireball_group = pygame.sprite.Group()

        # note: no need to keep your own array in sprite groups, just attach to group
        for dist_position in [1, 0.75, 0.5, 0.25]:
            self.fireball_sprite = Fireball(
                FireballParams(
                    # x_pos=dist_position * 100,
                    group=self.fireball_group,
                    # center_point=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                    center_point=(200, 200),
                    dist_from_center=dist_position,
                    outer_ball_center=self.rope_circle_radius - 70,
                )
            )

    def handle_main_menu_click(self):
        self.game_state_manager.set_state("main_menu")

    # this can now adequetly reset the game from anywhere.
    def reset(self):
        print("class Level: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.rope_active = False
        self.current_angle = starting_rope_angle
        self.angular_velocity = 0.11
        self.rotations_completed = 0
        self.player = Player(PlayerParams(coordinates=(250, SCREEN_HEIGHT - 150)))

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()

    def receive_player_input(self, input_type: str):
        if input_type == "space":
            self.rope_active = True
            self.player.receive_jump_input()

    # NOTE: does this need to be done for each fireball? might be able to just
    # do once for outer and then calc dist between those 2 points for other centers
    def calc_fireball_pos(self, center_offset, sin_angle, cos_angle):
        dist_from_center = self.outermost_fireball_pos * center_offset

        return [
            round(self.rope_circle_pos[0] + dist_from_center * sin_angle),
            round(self.rope_circle_pos[1] + dist_from_center * cos_angle),
        ]

    def variable_rope_speed_change(self):
        if (
            random.randint(
                1, 8
            )  # < smaller the second number, the more often speed changes
            < self.rotations_completed - self.last_speed_change_rotation
        ):
            self.last_speed_change_rotation = self.rotations_completed

            if self.active_rope_speed == "medium":
                if random.choice([True, False]):
                    self.active_rope_speed = "slow"
                    self.angular_velocity = rope_speeds["slow"]
                else:
                    self.active_rope_speed = "fast"
                    self.angular_velocity = rope_speeds["fast"]

            if self.active_rope_speed == "slow":
                if random.choice([True, False]):
                    self.active_rope_speed = "medium"
                    self.angular_velocity = rope_speeds["medium"]
                else:
                    self.active_rope_speed = "fast"
                    self.angular_velocity = rope_speeds["fast"]

            if self.active_rope_speed == "fast":
                if random.choice([True, False]):
                    self.active_rope_speed = "medium"
                    self.angular_velocity = rope_speeds["medium"]
                else:
                    self.active_rope_speed = "slow"
                    self.angular_velocity = rope_speeds["slow"]

    def run(self, delta_time):
        self.screen.blit(self.bg_image, (0, 0))

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

        self.screen.blit(self.fireball_image, fireball_rect)
        self.screen.blit(self.fireball_image, fireball_rect_2)
        self.screen.blit(self.fireball_image, fireball_rect_3)
        self.screen.blit(self.fireball_image, fireball_rect_4)

        # detect player death
        if not self.player.killed:
            if (
                fireball_rect.colliderect(self.player.rect)
                and self.player.jump_height < 100
            ):
                self.player.killed = True
                self.game_over = True
                self.rope_active = False
                self.end_game_menu.receive_and_calc_score(self.rotations_completed)

        if self.player.active and self.rope_active:
            if fireball_rect.colliderect(self.player.player_idle_spot):
                self.rope_passing_started = True
            else:
                if self.rope_passing_started:
                    self.rotations_completed += 1

                    self.variable_rope_speed_change()

                self.rope_passing_started = False

        self.monster_easement.update(delta_time)
        self.monster_rect.centerx = round(self.monster_easement.current_position)

        self.screen.blit(self.scaled_monster_image, self.monster_rect)

        if self.game_over:
            self.screen.blit(self.game_over_message, self.game_over_rect)
            self.end_game_menu.update()
            self.end_game_menu.draw(self.screen)
            # Note: Still not able to change speed from the easment class
        elif not self.rope_active:
            self.screen.blit(self.start_message, self.start_message_rect)

        if self.player.active:
            self.player.update(delta_time)
            self.player.draw(self.screen)

        self.fireball_group.update(
            FireballUpdateParams(
                delta=delta_time,
                angles=FireballPosParams(cos_angle=cos_angle, sin_angle=sin_angle),
            )
        )
        # )  # < Huge perk, auto calls on the whole group. don't need to loop
        self.fireball_group.draw(self.screen)
