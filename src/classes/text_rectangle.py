# an extension of Rectangle class that renders centered text inside
import pygame

from .rectangle import Rectangle, RectangleParams


class TextRectangleParams(RectangleParams):
    text: str
    text_color: tuple = (0, 0, 0)  # Default to black


class TextRectangle(Rectangle):
    def __init__(self, text_rectangle_params: TextRectangleParams):
        text_rectangle_params.entity_type = "text_rectangle"
        super().__init__(text_rectangle_params)
        self.text = text_rectangle_params.text
        self.text_color = text_rectangle_params.text_color
        self.font = pygame.font.Font(None, 30)  # Default font and size

    # this is interesting because it combined the super()'s draw method and then
    # add's tit's own text rendering on top
    def draw(self, surface):
        super().draw(surface)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
