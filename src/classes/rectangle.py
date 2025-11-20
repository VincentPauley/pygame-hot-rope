from typing import Optional

import pygame
from pydantic import BaseModel

from .entity import Entity, EntityParams


class RectangleParams(BaseModel):
    # this really doesn't need to specify entity params as long as it mandates EntitParams in the definition
    entity_params: Optional[EntityParams] = EntityParams(entity_type="rectangle")
    width: int
    height: int


class Rectangle(Entity):
    def __init__(
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
