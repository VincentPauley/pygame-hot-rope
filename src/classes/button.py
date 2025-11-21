import pygame

from .entity import Entity, EntityParams

pygame.font.init()
font = pygame.font.Font(
    None, 30
)  # move this into class to control font size per button


class Button(Entity):
    def __init__(
        self, text, onclick, color=(255, 255, 255), coords=(0, 0), dimensions=(10, 10)
    ):
        super().__init__(EntityParams(entity_type="ui", group_name="buttons"))
        self.color = color
        self.x = coords[0]
        self.y = coords[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text = text
        self.onclick = onclick

    # TODO: hover state detection
    def detect_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.onclick()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
