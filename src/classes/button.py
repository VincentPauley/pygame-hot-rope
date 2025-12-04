import pygame

from .entity import Entity, EntityParams

pygame.font.init()
font = pygame.font.Font(
    None, 30
)  # move this into class to control font size per button

# TODO: should button be an extension of rectangle?


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
        self.pressed = False

    def check_for_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                self.pressed = True
            if not mouse_pressed[0] and self.pressed:
                self.onclick()
                self.pressed = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
