import pygame

from assets import AssetManager
from classes.button import Button
from colors import COLOR_PRIMARY_BLUE
from config import game_config

font = pygame.font.SysFont("Arial", 50)

# up next: get star displays and logic into the end game menu
# figure out the free fireball logic and make scoring incorporate it
# multi-animations for frog and monster.


class EndGameMenu:
    score = 0
    stars = 0

    def __init__(self, main_menu_handler, reset_handler):
        self.asset_manager = AssetManager()
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

        self.empty_star_image = self.asset_manager.get_image("empty_star")
        self.star_image = self.asset_manager.get_image("star")

        # all stars set to empty at base
        self.star_one_image = self.empty_star_image
        self.star_two_image = self.empty_star_image
        self.star_three_image = self.empty_star_image

        self.retry_button.rect.right = self.inner_rect.centerx - 10
        self.main_menu_button.rect.left = self.inner_rect.centerx + 10

        self.main_menu_button.rect.bottom = self.inner_rect.bottom - 20
        self.retry_button.rect.bottom = self.inner_rect.bottom - 20

        self.score_display = font.render(f"Score: {str(self.score)}", True, "black")

        self.score_disply_rect = self.score_display.get_rect(
            center=(self.inner_rect.centerx, self.inner_rect.top + 50)
        )

        # split all this into it's own function now.

        self.middle_star_rect = self.empty_star_image.get_rect()

        self.middle_star_rect.centerx = self.score_disply_rect.centerx
        self.middle_star_rect.centery = self.score_disply_rect.bottom + 100

        self.left_star_rect = self.empty_star_image.get_rect()

        # other 2 stars are
        self.left_star_rect.centerx = self.middle_star_rect.centerx - 120
        self.left_star_rect.centery = self.middle_star_rect.centery

        self.right_star_rect = self.empty_star_image.get_rect()

        self.right_star_rect.centerx = self.middle_star_rect.centerx + 120
        self.right_star_rect.centery = self.middle_star_rect.centery

    def receive_and_calc_score(self, rotations_survived):
        self.score = rotations_survived * 10

        self.star_one_image = self.empty_star_image
        self.star_two_image = self.empty_star_image
        self.star_three_image = self.empty_star_image

        if self.score >= game_config.star_values.three:
            self.stars = 3
            self.star_one_image = self.star_image
            self.star_two_image = self.star_image
            self.star_three_image = self.star_image
        elif self.score >= game_config.star_values.two:
            self.stars = 2
            self.star_one_image = self.star_image
            self.star_two_image = self.star_image
        elif self.score >= game_config.star_values.one:
            self.stars = 1
            self.star_one_image = self.star_image

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

        # these just need to know which image to blit based on score
        surface.blit(self.star_one_image, self.left_star_rect)
        surface.blit(self.star_two_image, self.middle_star_rect)
        surface.blit(self.star_three_image, self.right_star_rect)
