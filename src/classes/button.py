import pygame

pygame.font.init()
font = pygame.font.Font(
    None, 30
)  # move this into class to control font size per button


class Button:
    width = 200
    height = 50
    x = 0
    y = 0
    color = (100, 200, 150)
    # text = "Click Me"

    rect = pygame.Rect(x, y, width, height)

    def __init__(self, text):
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
