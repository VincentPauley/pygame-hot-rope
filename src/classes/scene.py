import pygame
from pydantic import BaseModel

from assets import AssetManager


class SceneConfig(BaseModel):
    screen: 'pygame.Surface'

    class Config:
        arbitrary_types_allowed = True


class Scene:
    def __init__(self, config: SceneConfig):
        self.screen = config.screen
        self.asset_manager = AssetManager()
