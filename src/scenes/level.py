import pygame

from classes.button import Button
from colors import COLOR_PRIMARY_BLUE
from config import game_config

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]


class Level:
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
        self.player_color = "deepskyblue1"
        self.player = pygame.Rect(300, SCREEN_HEIGHT - 150, 50, 50)

        # pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self):
        print("class Level: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()

    def run(self, delta_time):
        self.main_menu_button.check_for_click()
        self.screen.fill("darkseagreen4")
        self.main_menu_button.draw(self.screen)
        pygame.draw.rect(self.screen, self.player_color, self.player)
