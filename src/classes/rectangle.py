import pygame


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 200
        self.y = 200

    def draw(self, surface):
        pygame.draw.rect(
            surface, (255, 0, 0), (self.x, self.y, self.width, self.height)
        )
