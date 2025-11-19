import pygame

pygame.font.init()
font = pygame.font.Font(
    None, 30
)  # move this into class to control font size per button


class Button:
    width = 200
    height = 50
    color = (100, 200, 150)

    def __init__(self, text, onclick, coords=(0, 0)):
        self.x = coords[0]
        self.y = coords[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text = text
        self.onclick = onclick

    # TODO: hover state detection
    def detect_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.onclick()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
