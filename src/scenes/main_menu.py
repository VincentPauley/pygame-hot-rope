import pygame

from classes.button import Button
from colors import COLOR_PRIMARY_YELLOW
from config import config

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]


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


class MainMenu:
    active_ticks = 0
    starting_ticks = 0

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
                        "rebounder_experiment"  # TODO: these should be passed in somehow rather than hard-coded
                    ),
                },
                # NOTE: this is causing issues with quitting since another frame is attempted
                {"text": "Quit", "onclick": lambda: pygame.quit()},
            ],
        )

    def reset(self):
        print("class MainMenu: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()
        # needs to clear task from game scene manager once completed

    # called on every frame
    # get current_scene_start out of params and into the reset function
    def run(self, delta_time):
        self.active_ticks = pygame.time.get_ticks() - self.starting_ticks
        self.screen.fill("dodgerblue")
        for button in self.main_menu_buttons:
            button.check_for_click()
            button.draw(self.screen)
