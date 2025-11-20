from typing import Optional

import pygame
from pydantic import BaseModel

from .entity import Entity, EntityParams


class RectangleParams(BaseModel):
    entity_params: Optional[EntityParams] = EntityParams(
        entity_type="rectangle", group_name="rectangles"
    )
    width: int
    height: int


defaultEntityDetails = {
    "id": "rect_01",
    "group_name": "rectangles",
    "entity_type": "shape",
}


class Rectangle(Entity):
    def __init__(
        # self, entityDetails=defaultEntityDetails, width=10, height=10, color=(255, 0, 0)
        self,
        rectangle_params: RectangleParams,
        color=(255, 0, 0),
    ):
        # TODO: id should be unique and auto generated if not provided (probably within entity class)
        # print("entityDetails:", entityDetails)
        super().__init__(rectangle_params.entity_params)
        self.width = rectangle_params.width
        self.height = rectangle_params.height
        self.x = 200
        self.y = 200
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
