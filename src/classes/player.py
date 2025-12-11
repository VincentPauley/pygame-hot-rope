import os
from typing import Any, Optional

import pygame
from pydantic import BaseModel

image_path = os.path.join("src", "assets", "froggy.png")


class PlayerParams(BaseModel):
    color: Optional[str] = "royalblue"
    width: Optional[int] = 50
    height: Optional[int] = 50
    starting_rect: Any
    # for debug
    draw_hit_box: Optional[bool] = False
    draw_starting_box: Optional[bool] = False


class Player(pygame.sprite.Sprite):
    def __init__(self, params: PlayerParams):
        # TODO: width/height probably don't need to be stored as indvidual keys, accessible from rect.
        self.width = params.width
        self.height = params.height
        self.color = params.color
        self.draw_hit_box = params.draw_hit_box
        self.draw_starting_box = params.draw_starting_box
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(
            center=(params.starting_rect.x, params.starting_rect.y + self.height / 2)
        )
        self.starting_rect = params.starting_rect
        # non param fields
        self.y_velocity = 0
        self.x_velocity = 0
        self.gravity = 1
        self.is_jumping = False
        self.jump_height = 0  # < can now use this for determining collision in more human readable way.
        self.killed = False
        self.active = True  # update & draw functions will only run when active
        self.player_radius = min(self.rect.width, self.rect.height) // 2

    def calc_player_shadow_rect(self):
        shadow = pygame.Rect(
            self.starting_rect.x,
            self.starting_rect.y + self.height / 2,  # position just under player
            self.width + self.jump_height * 0.3,
            self.height * 0.8,
        )

        shadow.centerx = self.rect.centerx

        return shadow

    def receive_jump_input(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -20

    def update(self, delta_time):
        if self.killed and self.rect.right < 0:
            self.active = False
        if self.killed:
            self.y_velocity = -5
            self.x_velocity = -22
            self.rect.y += self.y_velocity * delta_time * 60
            self.rect.x += self.x_velocity * delta_time * 60
        if self.is_jumping:
            self.y_velocity = self.y_velocity + self.gravity
            self.rect.y += self.y_velocity * delta_time * 60
            self.jump_height = self.starting_rect.y - self.rect.y
            # player is back on ground, stop jump and reset
            if self.rect.y >= self.starting_rect.y:
                self.rect.y = self.starting_rect.y
                # reset internals
                self.is_jumping = False
                self.y_velocity = 0
                self.jump_height = 0

    # TODO: lookup how to define surface in pydantic model so it doesn't need to be a param
    # every time. Maybe that becomes part of the entity class?
    def draw(self, surface):
        if self.draw_starting_box:
            pygame.draw.rect(
                surface,
                "red",
                self.starting_rect,
            )

        if not self.killed:
            pygame.draw.ellipse(
                surface,
                "orange",
                self.calc_player_shadow_rect(),
            )

        surface.blit(self.image, self.rect)

        if self.draw_hit_box:
            pygame.draw.rect(surface, "red", self.rect, 2)
