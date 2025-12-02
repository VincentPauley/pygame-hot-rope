from typing import Optional, Tuple

import pygame
from pydantic import BaseModel


class PlayerParams(BaseModel):
    coordinates: Optional[Tuple[int, int]] = (0, 0)
    color: Optional[str] = "green"
    width: Optional[int] = 50
    height: Optional[int] = 50


class Player:
    def __init__(self, params: PlayerParams):
        # TODO: width/height probably don't need to be stored as indvidual keys, accessible from rect.
        self.width = params.width
        self.height = params.height
        self.color = params.color
        self.starting_coords = params.coordinates
        # non param fields
        self.velocity = 0
        self.gravity = 1
        self.is_jumping = False

        self.rect = pygame.Rect(
            params.coordinates[0],
            params.coordinates[1],
            self.width,
            self.height,
        )

        self.player_radius = min(self.rect.width, self.rect.height) // 2

    def receive_jump_input(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -20

    def update(self, delta_time):
        if self.is_jumping:
            self.velocity = self.velocity + self.gravity
            self.rect.y += self.velocity * delta_time * 60
            # player is back on ground, stop jump and reset
            if self.rect.y >= self.starting_coords[1]:
                self.rect.y = self.starting_coords[1]
                self.is_jumping = False
                self.velocity = 0

    # TODO: lookup how to define surface in pydantic model so it doesn't need to be a param
    # every time. Maybe that becomes part of the entity class?
    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self.rect)

        # draw player as a circle for the time being...
        pygame.draw.circle(surface, self.color, self.rect.center, self.player_radius)
