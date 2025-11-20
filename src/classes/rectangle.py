from typing import Optional

import pygame
from pydantic import BaseModel

from .entity import Entity, EntityParams


class RectangleParams(BaseModel):
    group_name: Optional[str] = None
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
        super().__init__(
            EntityParams(
                # NOTE: entity type is hard-coded here on purpose so that all Rectangle instances have the same type
                # in the future this could be overwritten by a super-ceding class if desired.
                group_name=rectangle_params.group_name,
                entity_type="rectangle",
            )
        )
        self.width = rectangle_params.width
        self.height = rectangle_params.height
        self.x = 200
        self.y = 200
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
