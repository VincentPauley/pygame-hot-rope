# this serves as a popup modal once game over is hit to display score
# and allow for the user to either restart or go back to main menu
import pygame

from classes.button import Button
from config import game_config


class EndGameMenu:
    def __init__(self, main_menu_handler, reset_handler):
        self.outer_rect = pygame.Rect(
            0,
            0,
            game_config.window.size["width"] * 0.8,
            game_config.window.size["height"] * 0.8,
        )

        self.outer_rect.center = (
            game_config.window.size["width"] // 2,
            game_config.window.size["height"] // 2,
        )

        self.main_menu_button = Button(
            "Main Menu",
            lambda: main_menu_handler(),
            (200, 200, 200),
            (self.outer_rect.centerx - 100, 140),
            (200, 50),
        )
        self.retry_button = Button(
            "Retry",
            lambda: reset_handler(),
            (200, 200, 200),
            (self.outer_rect.centerx - 100, 220),
            (200, 50),
        )

    # def handle_main_click(self):
    #     print("hande main click")

    def update(self):
        self.main_menu_button.check_for_click()
        self.retry_button.check_for_click()

    def draw(self, surface):
        pygame.draw.rect(surface, "black", self.outer_rect)

        self.main_menu_button.draw(surface)
        self.retry_button.draw(surface)
