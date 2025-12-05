import os
from typing import Any, Tuple

import pydantic
import pygame

image_path = os.path.join("src", "assets", "fireball.png")


class FireballParams(pydantic.BaseModel):
    group: Any
    center_point: Tuple[int, int]


class Fireball(pygame.sprite.Sprite):
    def __init__(self, fireballParams: FireballParams):
        super().__init__(fireballParams.group)

        print("centerpoint: ", fireballParams.center_point)

        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect(center=(100, 100))

    def update(self, delta):
        self.rect.y += 2 * delta * 60
