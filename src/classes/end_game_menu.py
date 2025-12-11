import pygame

from classes.button import Button
from colors import COLOR_PRIMARY_BLUE
from config import game_config

font = pygame.font.SysFont("Arial", 50)

# up next: get star displays and logic into the end game menu
# figure out the free fireball logic and make scoring incorporate it
# multi-animations for frog and monster.


class EndGameMenu:
    score = 0

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

        self.score_display = font.render(f"Score: {str(self.score)}", True, "black")

        self.score_disply_rect = self.score_display.get_rect(
            center=(self.inner_rect.centerx, self.inner_rect.top + 50)
        )

        self.middle_star_rect = pygame.Rect(0, 0, 100, 100)
        self.middle_star_rect.centerx = self.score_disply_rect.centerx
        self.middle_star_rect.centery = self.score_disply_rect.bottom + 100

    def receive_and_calc_score(self, rotations_survived):
        self.score = rotations_survived * 10
        self.score_display = font.render(f"Score: {str(self.score)}", True, "black")

        self.score_disply_rect = self.score_display.get_rect(
            center=(self.inner_rect.centerx, self.inner_rect.top + 50)
        )

    def update(self):
        self.main_menu_button.check_for_click()
        self.retry_button.check_for_click()

    def draw(self, surface):
        pygame.draw.rect(surface, "azure2", self.outer_rect, border_radius=10)
        pygame.draw.rect(surface, "azure3", self.inner_rect, border_radius=5)
        self.main_menu_button.draw(surface)
        self.retry_button.draw(surface)
        surface.blit(self.score_display, self.score_disply_rect)

        pygame.draw.rect(surface, "gold", self.middle_star_rect)
