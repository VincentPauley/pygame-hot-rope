import math
import random

import pygame

from classes.button import Button
from classes.moveable_rectangle import MoveableRectangle, MoveableRectangleParams
from colors import COLOR_PRIMARY_BLUE, COLOR_PRIMARY_YELLOW
from config import config

FONT_NAME = "Arial"

font = pygame.font.SysFont(FONT_NAME, 30)

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]


class RebounderExperiment:
    active_ticks = 0
    starting_ticks = 0
    velo_balls = []
    fire_ball_dimensions = (20, 20)

    def create_fireballs(self):
        ball_count = 10

        y_increment = SCREEN_HEIGHT / ball_count
        x_increment = SCREEN_WIDTH / ball_count

        for i in range(ball_count):
            speed_multiplier = random.randint(1, 6)

            velo_speed = 80 * speed_multiplier

            random_effect_1 = 1 if random.randint(1, 2) == 1 else -1
            random_effect_2 = 1 if random.randint(1, 2) == 1 else -1

            self.velo_balls.append(
                MoveableRectangle(
                    MoveableRectangleParams(
                        group_name="velo_ball",
                        width=self.fire_ball_dimensions[0],
                        height=self.fire_ball_dimensions[1],
                        coordinates=(i * x_increment, i * y_increment),
                        color=COLOR_PRIMARY_YELLOW,
                        velocity=(
                            velo_speed * random_effect_1,
                            velo_speed * random_effect_2,
                        ),
                    )
                )
            )

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.screen = display_screen
        self.game_state_manager = game_state_manager
        self.main_menu_button = Button(
            "Main Menu",
            lambda: game_state_manager.set_state("main_menu"),
            COLOR_PRIMARY_BLUE,
            (10, 10),
            (150, 50),
        )

        self.create_fireballs()
        self.timer_rect = pygame.Rect(SCREEN_WIDTH - (100 + 10), 10, 100, 50)

    def reset(self):
        print("class RebounderExperiment: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    # can now make specific handlers per task like reset or setup to minimize what's needed
    # inside of the run function itself :)
    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()

    # called on every frame
    def run(self, delta_time):
        self.active_ticks = pygame.time.get_ticks() - self.starting_ticks

        self.screen.fill("orange")

        for velo_ball in self.velo_balls:
            if velo_ball.rect.right >= SCREEN_WIDTH and velo_ball.x_velocity > 0:
                velo_ball.reverse_x_velo()
            if velo_ball.rect.left <= 0 and velo_ball.x_velocity < 0:
                velo_ball.reverse_x_velo()
            if velo_ball.rect.bottom >= SCREEN_HEIGHT and velo_ball.y_velocity > 0:
                velo_ball.reverse_y_velo()
            if velo_ball.rect.top <= 0 and velo_ball.y_velocity < 0:
                velo_ball.reverse_y_velo()

            velo_ball.update_pos(delta_time)

        for velo_ball in self.velo_balls:
            velo_ball.draw(self.screen)

        pygame.draw.rect(self.screen, "gray24", self.timer_rect)

        timer_text_surface = font.render(
            str(math.floor(self.active_ticks / 1000)), True, "White"
        )

        # to move this out of run function would need to preset how the size and rect is treated.
        timer_text_rect = timer_text_surface.get_rect(center=self.timer_rect.center)

        self.screen.blit(timer_text_surface, timer_text_rect)

        self.main_menu_button.check_for_click()
        self.main_menu_button.draw(self.screen)
