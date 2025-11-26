import math
import sys

import pygame

from classes.button import Button
from config import config

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]
FPS = 60
FONT_NAME = "Arial"

# custom colors
COLOR_PRIMARY_ORANGE = (255, 118, 35)
COLOR_PRIMARY_YELLOW = (241, 245, 72)
COLOR_PRIMARY_BLUE = (73, 114, 238)

font = pygame.font.SysFont(FONT_NAME, 30)


def handle_quit():
    print("main_2.py handle quit")
    # scene_manager.running = False
    pygame.quit()
    sys.exit()


class Game:
    active_scene_started_at = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager("main_menu")

        self.main_menu = MainMenu(self.screen, self.game_state_manager)
        self.rebounder_experiment = RebounderExperiment(
            self.screen, self.game_state_manager
        )

        # this dictionary stores every scene by it's key name
        self.state_map = {
            "main_menu": self.main_menu,
            "rebounder_experiment": self.rebounder_experiment,
        }

    def update_started_at(self, ticks):
        self.started_at = ticks

    def run(self):
        while True:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.state_map[self.game_state_manager.get_state()].run(
                delta_time,
                pygame.time.get_ticks(),
                self.game_state_manager.current_scene_start,
            )

            pygame.display.flip()


def define_button_group(
    container_dimensions=(0, 0),
    orientation="vertical",
    button_width=300,
    button_height=60,
    buttons=[],
):
    # orientation "vertical" | "horizontal"
    # inner_margin: "int" (separate buttons buy)
    # buttons

    group_entities = []

    container_width = container_dimensions[0]
    container_height = container_dimensions[1]

    inner_margin = 10

    gutter_count = len(buttons) - 1

    group_height = len(buttons) * button_height + gutter_count * inner_margin

    container_y = (container_height - group_height) / 2
    container_x = (container_width - button_width) / 2

    for index, button in enumerate(buttons):
        button_y = container_y + index * (button_height + inner_margin)
        button_x = container_x  # < TODO: center to container
        group_entities.append(
            Button(
                button["text"],
                button["onclick"],
                COLOR_PRIMARY_YELLOW,
                (button_x, button_y),
                (button_width, button_height),
            )
        )

    return group_entities


# TODO: move to independent scene file
class MainMenu:
    game_ticks = 0
    active_ticks = 0

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.game_state_manager = game_state_manager

        self.main_menu_buttons = define_button_group(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            "vertical",
            400,
            60,
            [
                {
                    "text": "Start Game",
                    "onclick": lambda: game_state_manager.set_state(
                        "rebounder_experiment", self.game_ticks
                    ),
                },
                {"text": "Quit", "onclick": handle_quit},
            ],
        )

    # called on every frame
    def run(self, delta_time, ticks, current_scene_start):
        self.game_ticks = ticks
        self.active_ticks = ticks - current_scene_start
        self.screen.fill("dodgerblue")
        for button in self.main_menu_buttons:
            button.check_for_click()
            button.draw(self.screen)


# TODO: move to independent scene file
class RebounderExperiment:
    game_ticks = 0
    active_ticks = 0

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.screen = display_screen
        self.game_state_manager = game_state_manager
        self.main_menu_button = Button(
            "Main Menu",
            lambda: game_state_manager.set_state("main_menu", self.game_ticks),
            COLOR_PRIMARY_BLUE,
            (10, 10),
            (150, 50),
        )

        self.timer_rect = pygame.Rect(SCREEN_WIDTH - (100 + 10), 10, 100, 50)

    # called on every frame
    def run(self, delta_time, ticks, current_scene_start):
        self.game_ticks = ticks
        self.active_ticks = ticks - current_scene_start

        self.screen.fill("orange")

        pygame.draw.rect(self.screen, "gray24", self.timer_rect)

        timer_text_surface = font.render(
            str(math.floor(self.active_ticks / 1000)), True, "White"
        )

        time_text_rect = timer_text_surface.get_rect(center=self.timer_rect.center)

        self.screen.blit(timer_text_surface, time_text_rect)

        self.main_menu_button.check_for_click()
        self.main_menu_button.draw(self.screen)


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        self.current_scene_start = 0

    def get_state(self):
        return self.currentState

    def set_state(self, newState, ticks):
        self.currentState = newState
        self.current_scene_start = ticks


if __name__ == "__main__":
    game = Game()
    game.run()
