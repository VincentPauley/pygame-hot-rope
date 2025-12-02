from typing import Optional

import pygame
from pydantic import BaseModel


class PlayerParams(BaseModel):
    color: Optional[str] = "green"
    width: Optional[int] = 50
    height: Optional[int] = 50


class Player:
    def __init__(self, params: PlayerParams):
        # TODO: these probably don't need to be stored as indvidual keys, accessible from rect.
        self.width = params.width
        self.height = params.height
        self.color = params.color

        self.rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height,
        )

    # TODO: lookup how to define surface in pydantic model so it doesn't need to be a param
    # every time. Maybe that becomes part of the entity class?
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
