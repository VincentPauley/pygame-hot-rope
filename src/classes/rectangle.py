import pygame

from .entity import Entity


class Rectangle(Entity):
    def __init__(self, width, height, color=(255, 0, 0)):
        super().__init__("rectangle", "shape", "rectangles")
        self.width = width
        self.height = height
        self.x = 200
        self.y = 200
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
