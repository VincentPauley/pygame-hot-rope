import pygame

from classes.button import Button
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
    active_scene = "main_menu"
    running = True

    def __init__(self):
        pass

    def register_scene(self, key, scene):
        self.scenes[key] = scene
        self.scene_keys.append(key)

    def change_scene(self, scene_key):
        # scene_keys = []
        print("change scene: ", scene_key)
        self.active_scene = scene_key

    def run(self):
        while self.running:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         print("quit detected")
            #         self.running = False
            #         handle_quit()
            #         return
            # keyboard interrupt is not working from here yet...
            try:
                self.scenes[self.active_scene].draw()
                self.scenes[self.active_scene].process_events()
            except KeyboardInterrupt:
                print("keyboard interrupt detected")
                self.running = False
                handle_quit()
                return


def handle_quit():
    print("main.py handle quit")
    scene_manager.running = False
    pygame.quit()


# last key piece is to be able to pass in the content of a scene and have it all
# rendered by the same loop - start with the button

scene_manager = SceneManager()
# NOTE:
# could be that the content of a scene is just a function that gets called every
# iteration and receives delta?

# note: lambda creates a zero arg function to be called by the Button with param: "Game"
main_menu = Scene(
    {
        "screen": screen,
        "handle_quit": handle_quit,
        "entities": [Button("Start Game", lambda: scene_manager.change_scene("game"))],
    }
)
game = Scene(
    {
        "screen": screen,
        "handle_quit": handle_quit,
        "entities": [
            Button("Main Menu", lambda: scene_manager.change_scene("main_menu"))
        ],
        "bg_color": (50, 50, 150),
    }
)

scene_manager.register_scene("main_menu", main_menu)
scene_manager.register_scene("game", game)

scene_manager.running = True
scene_manager.run()
