import pygame

from .entity import Entity, EntityParams

defaultEntityDetails = {
    "id": "rect_01",
    "entity_type": "shape",
    "group_name": "rectangles",
}


class Rectangle(Entity):
    def __init__(
        self, entityDetails=defaultEntityDetails, width=10, height=10, color=(255, 0, 0)
    ):
        # TODO: id should be unique and auto generated if not provided (probably within entity class)
        # print("entityDetails:", entityDetails)
        super().__init__(EntityParams(entity_type="rectangle", group_name="rectangles"))
        self.width = width
        self.height = height
        self.x = 200
        self.y = 200
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
