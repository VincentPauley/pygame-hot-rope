from typing import Optional, Tuple

import pygame
from pydantic import BaseModel

from .entity import Entity, EntityParams


class RectangleParams(BaseModel):
    # supers
    group_name: Optional[str] = None
    entity_type: Optional[str] = "rectangle"
    # specifics
    coordinates: Optional[Tuple[int, int]] = (0, 0)
    color: Optional[Tuple[int, int, int]] = (255, 255, 255)
    width: int
    height: int


# this class strategy sort of locks away a rect that is used in tandum with a surface to blit
class Rectangle(Entity):
    def __init__(self, rectangle_params: RectangleParams):
        # TODO: id should be unique and auto generated if not provided (probably within entity class)
        # print("entityDetails:", entityDetails)
        super().__init__(
            EntityParams(
                # NOTE: entity type is hard-coded here on purpose so that all Rectangle instances have the same type
                # in the future this could be overwritten by a super-ceding class if desired.
                group_name=rectangle_params.group_name,
                entity_type=rectangle_params.entity_type,
            )
        )

        self.color = rectangle_params.color
        self.rect = pygame.Rect(
            rectangle_params.coordinates[0],
            rectangle_params.coordinates[1],
            rectangle_params.width,
            rectangle_params.height,
        )

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
