import os

import pygame


# This class handles all of the optimized loading of images
# so that the other classes & scenes don't need to worry about
# file paths or project structures.  Instead just retrieve image
# by it's key to pull it into scene/class.
#
class AssetManager:
    def __init__(self):
        self.assets_dir = os.path.join("src", "assets")
        self.images = {}
        self.load_images()

    # NOTE: for now this is fine but could benefit from scene-specific loading
    def load_images(self):
        """Load all images once at startup"""
        self._register_image("froggy", "froggy.png")
        self._register_image("fireball", "fireball.png")
        self._register_image("star", "star.png")
        self._register_image("empty_star", "empty-star.png")
        self._register_image("monster", "hot-rope-monster.png")
        self._register_image("main_title", "hot-rope-title.png")
        self._register_image("beach_bg", "beach-bg.png", False)
        self._register_image("foreground", "foreground-bushes.png")

    def _register_image(self, image_name, image_filename, transparent=True):
        loaded_asset = pygame.image.load(self._path(image_filename))

        converted_asset = (
            loaded_asset.convert_alpha() if transparent else loaded_asset.convert()
        )

        self.images[image_name] = converted_asset

    def _path(self, filename):
        return os.path.join(self.assets_dir, filename)

    def get_image(self, name):
        return self.images[name]
