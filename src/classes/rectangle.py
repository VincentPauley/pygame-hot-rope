from typing import Optional, Tuple

import pygame
from pydantic import BaseModel

from .entity import Entity, EntityParams


class RectangleParams(BaseModel):
    group_name: Optional[str] = None
    coordinates: Optional[Tuple[int, int]] = (0, 0)
    color: Optional[Tuple[int, int, int]] = (255, 255, 255)
    width: int
    height: int


class Rectangle(Entity):
    def __init__(self, rectangle_params: RectangleParams):
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
        self.x = rectangle_params.coordinates[0]
        self.y = rectangle_params.coordinates[1]
        self.color = rectangle_params.color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
