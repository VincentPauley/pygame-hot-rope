# this serves as a popup modal once game over is hit to display score
# and allow for the user to either restart or go back to main menu
import pygame

from classes.button import Button
from colors import COLOR_PRIMARY_BLUE
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

        self.inner_rect = pygame.Rect(
            self.outer_rect.x + 10,
            self.outer_rect.y + 10,
            self.outer_rect.width - 20,
            self.outer_rect.height - 20,
        )

        self.main_menu_button = Button(
            "Main Menu",
            lambda: main_menu_handler(),
            COLOR_PRIMARY_BLUE,
            (0, 0),
            (200, 50),
        )
        self.retry_button = Button(
            "Retry",
            lambda: reset_handler(),
            COLOR_PRIMARY_BLUE,
            (0, 0),
            (200, 50),
        )

        self.retry_button.rect.right = self.inner_rect.centerx - 10
        self.main_menu_button.rect.left = self.inner_rect.centerx + 10

        self.main_menu_button.rect.bottom = self.inner_rect.bottom - 20
        self.retry_button.rect.bottom = self.inner_rect.bottom - 20

    def update(self):
        self.main_menu_button.check_for_click()
        self.retry_button.check_for_click()

    def draw(self, surface):
        pygame.draw.rect(surface, "azure2", self.outer_rect, border_radius=10)
        pygame.draw.rect(surface, "azure3", self.inner_rect, border_radius=5)
        self.main_menu_button.draw(surface)
        self.retry_button.draw(surface)
