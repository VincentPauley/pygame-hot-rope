import pygame

from classes.button import Button
from classes.rectangle import Rectangle, RectangleParams
from classes.scene import Scene
from config import config

pygame.init()

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(config["window"]["caption"])

COLOR_PRIMARY_ORANGE = (255, 118, 35)
COLOR_PRIMARY_YELLOW = (241, 245, 72)


# button group configuration.
# maybe this becomes a class, but should let you pick container size along with strd opts
def define_button_group(
    container_dimensions=(0, 0),
    orientation="vertical",
    button_width=300,
    button_height=60,
    buttons=[],
):
    # orientation "vertical" | "horizontal"
    # inner_margin: "int" (separate buttons buy)
    # buttons

    group_entities = []

    container_width = container_dimensions[0]
    container_height = container_dimensions[1]

    inner_margin = 10

    gutter_count = len(buttons) - 1

    group_height = len(buttons) * button_height + gutter_count * inner_margin

    container_y = (container_height - group_height) / 2
    container_x = (container_width - button_width) / 2

    for index, button in enumerate(buttons):
        button_y = container_y + index * (button_height + inner_margin)
        button_x = container_x  # < TODO: center to container
        group_entities.append(
            Button(
                button["text"],
                button["onclick"],
                COLOR_PRIMARY_YELLOW,
                (button_x, button_y),
                (button_width, button_height),
            )
        )

    return group_entities


clock = pygame.time.Clock()


def handle_quit():
    print("main.py handle quit")
    scene_manager.running = False
    pygame.quit()


main_menu_buttons = define_button_group(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    "vertical",
    400,
    60,
    [
        {"text": "Start Game", "onclick": lambda: scene_manager.change_scene("game")},
        {"text": "Quit", "onclick": handle_quit},
    ],
)


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

    def change_scene(self, scene_key: str):
        if self.scene_keys.index(scene_key) < 0:
            raise ValueError(f"Scene key {scene_key} not registered: " + scene_key)
        self.active_scene = scene_key

    def run(self):
        while self.running:
            delta_time = clock.tick(60) / 1000

            try:
                self.scenes[self.active_scene].process_scene(delta_time)
                self.scenes[self.active_scene].draw()
                self.scenes[self.active_scene].process_events()
            except KeyboardInterrupt:
                print("keyboard interrupt detected")
                self.running = False
                handle_quit()
                return
            # TODO: more generic error handling from here


# last key piece is to be able to pass in the content of a scene and have it all
# rendered by the same loop - start with the button

scene_manager = SceneManager()


class MainMenu:
    entities = []

    def __init__(self):
        # main_menu_buttons
        for entity in main_menu_buttons:
            self.entities.append(entity)

        # add rectangles
        self.entities.append(
            Rectangle(
                RectangleParams(
                    group_name="rectangles", width=100, height=100, color=(0, 255, 255)
                )
            )
        )
        self.entities.append(
            Rectangle(RectangleParams(group_name="rectangles", width=20, height=70))
        )

    # called on every loop iteration
    def process(self, delta_time):
        # hard-coding effect for now
        speed = 50

        # move rectangles around
        rectangles = [
            entity for entity in self.entities if entity.group_name == "rectangles"
        ]

        for rectangle in rectangles:
            rectangle.x += delta_time * speed


main_menu_instance = MainMenu()


class GameScene:
    entities = []

    def __init__(self):
        self.entities.append(
            Rectangle(
                RectangleParams(
                    group_name="fireballs",
                    width=100,
                    height=100,
                    coordinates=(230, 78),
                    color=COLOR_PRIMARY_ORANGE,
                )
            )
        )
        self.entities.append(
            Rectangle(
                RectangleParams(
                    group_name="fireballs",
                    width=20,
                    height=20,
                    coordinates=(0, 150),
                    color=COLOR_PRIMARY_YELLOW,
                )
            )
        )
        self.entities.append(
            Button(
                "Main Menu",
                lambda: scene_manager.change_scene("main_menu"),
                COLOR_PRIMARY_YELLOW,
                (20, 50),
                (300, 50),
            )
        )

        print("-- game scene check --")
        print("entity_type: ", self.entities[0].entity_type)
        print("group_name: ", self.entities[0].group_name)

    def process(self, delta_time):
        fireballs = [
            entity for entity in self.entities if entity.group_name == "fireballs"
        ]

        for fireball in fireballs:
            fireball.x += delta_time * 100


game_scene_instance = GameScene()

main_menu = Scene(
    {
        "screen": screen,
        "handle_quit": handle_quit,
        "entities": main_menu_instance.entities,
        "process": main_menu_instance.process,
        "bg_color": COLOR_PRIMARY_ORANGE,
    }
)
game = Scene(
    {
        "screen": screen,
        "handle_quit": handle_quit,
        "entities": game_scene_instance.entities,
        "process": game_scene_instance.process,
        "bg_color": (50, 50, 150),
    }
)

scene_manager.register_scene("main_menu", main_menu)
scene_manager.register_scene("game", game)

scene_manager.running = True
scene_manager.run()
