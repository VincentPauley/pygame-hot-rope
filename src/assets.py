import os

import pygame


class AssetManager:
    def __init__(self):
        self.assets_dir = os.path.join("src", "assets")
        self.images = {}

    def load_images(self):
        """Load all images once at startup"""
        self.images["froggy"] = pygame.image.load(
            self._path("froggy.png")
        ).convert_alpha()
        self.images["monster"] = pygame.image.load(
            self._path("hot-rope-monster.png")
        ).convert_alpha()
        self.images["fireball"] = pygame.image.load(
            self._path("fireball.png")
        ).convert_alpha()
        self.images["star"] = pygame.image.load(self._path("star.png")).convert_alpha()
        self.images["main_title"] = pygame.image.load(
            self._path("hot-rope-title.png")
        ).convert_alpha()
        self.images["beach_bg"] = pygame.image.load(
            self._path("beach-bg.png")
        ).convert()

    def _path(self, filename):
        return os.path.join(self.assets_dir, filename)

    def get_image(self, name):
        return self.images[name]


# Example instance
# assets = AssetManager()
