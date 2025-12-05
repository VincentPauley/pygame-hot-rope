import os
from typing import Any, Tuple

import pydantic
import pygame

image_path = os.path.join("src", "assets", "fireball.png")


# NOTE: probably need a sibling class for rebounding fireballs later
class FireballParams(pydantic.BaseModel):
    dist_from_center: float
    group: Any
    center_point: Tuple[int, int]
    outer_ball_center: int


class FireballUpdateParams(pydantic.BaseModel):
    cos_angle: float
    sin_angle: float


class Fireball(pygame.sprite.Sprite):
    def __init__(self, fireballParams: FireballParams):
        super().__init__(fireballParams.group)

        self.image = pygame.image.load(image_path).convert_alpha()
        self.dist_from_center = fireballParams.dist_from_center

        # TODO: move back to under rect soon
        self.rect = self.image.get_rect(center=(self.dist_from_center, 100))

        self.center_point = fireballParams.center_point
        self.outer_ball_center = fireballParams.outer_ball_center

    def _calc_and_apply_position(self, params: FireballUpdateParams):
        base_dist = self.outer_ball_center * self.dist_from_center

        x = self.center_point[0] + base_dist * params.cos_angle
        y = self.center_point[1] + base_dist * params.sin_angle

        self.rect.center = (x, y)

    def update(self, delta, cos, sin):
        self.rect.y += 2 * delta * 60

        self._calc_and_apply_position(
            FireballUpdateParams(
                cos_angle=cos,
                sin_angle=sin,
            )
        )
