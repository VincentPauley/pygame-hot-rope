from typing import Optional, Tuple

import pygame
from pydantic import BaseModel


class PlayerParams(BaseModel):
    coordinates: Optional[Tuple[int, int]] = (0, 0)
    color: Optional[str] = "royalblue"
    width: Optional[int] = 50
    height: Optional[int] = 50
    # for debug
    draw_hit_box: Optional[bool] = False
    draw_starting_box: Optional[bool] = False


class Player:
    def __init__(self, params: PlayerParams):
        # TODO: width/height probably don't need to be stored as indvidual keys, accessible from rect.
        self.width = params.width
        self.height = params.height
        self.color = params.color
        self.starting_coords = params.coordinates
        self.draw_hit_box = params.draw_hit_box
        self.draw_starting_box = params.draw_starting_box
        # non param fields
        self.velocity = 0
        self.gravity = 1
        self.is_jumping = False
        self.jump_height = 0  # < can now use this for determining collision in more human readable way.

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
            self.jump_height = self.starting_coords[1] - self.rect.y
            # player is back on ground, stop jump and reset
            if self.rect.y >= self.starting_coords[1]:
                self.rect.y = self.starting_coords[1]
                # reset internals
                self.is_jumping = False
                self.velocity = 0
                self.jump_height = 0

    # TODO: lookup how to define surface in pydantic model so it doesn't need to be a param
    # every time. Maybe that becomes part of the entity class?
    def draw(self, surface):
        if self.draw_starting_box:
            pygame.draw.rect(
                surface,
                "blue",
                (
                    self.starting_coords[0],
                    self.starting_coords[1],
                    self.width,
                    self.height,
                ),
            )

        # draw player as a circle for the time being...
        pygame.draw.circle(surface, self.color, self.rect.center, self.player_radius)

        if self.draw_hit_box:
            pygame.draw.rect(surface, "red", self.rect, 2)
