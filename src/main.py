import pygame

from classes.scene import Scene
from config import config

pygame.init()

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(config["window"]["caption"])


class SceneManager:
    scenes = {}
    scene_keys = []

    def __init__(self):
        pass

    def register_scene(self, key, scene):
        self.scenes[key] = scene
        self.scene_keys.append(key)


main_menu = Scene({"screen": screen})
game = Scene({"screen": screen, "bg_color": (50, 50, 150)})

scene_manager = SceneManager()

scene_manager.register_scene("main_menu", main_menu)
scene_manager.register_scene("game", game)

scene_manager.scenes["main_menu"].activate()
