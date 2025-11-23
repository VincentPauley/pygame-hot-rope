import random

import pygame

from classes.button import Button
from classes.moveable_rectangle import MoveableRectangle, MoveableRectangleParams
from classes.scene import Scene
from config import config

pygame.init()

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption(config["window"]["caption"])

COLOR_PRIMARY_ORANGE = (255, 118, 35)
COLOR_PRIMARY_YELLOW = (241, 245, 72)
COLOR_PRIMARY_BLUE = (73, 114, 238)

# TODOS:

# reset/restart scene management
# timer available to ALL scenes (could be useful in )

timer_event = pygame.USEREVENT + 1  # Custom event ID for our timer
pygame.time.set_timer(timer_event, 1000)


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
            clock.tick(60)  # limit to 60 FPS
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


scene_manager = SceneManager()


class MainMenu:
    entities = []

    def __init__(self):
        # main_menu_buttons
        for entity in main_menu_buttons:
            self.entities.append(entity)

    # called on every loop iteration
    def process(self, delta_time):
        pass


main_menu_instance = MainMenu()


class GameScene:
    entities = []

    fire_ball_dimensions = (50, 50)

    def create_fireballs(self):
        ball_count = 10

        y_increment = SCREEN_HEIGHT / ball_count
        x_increment = SCREEN_WIDTH / ball_count

        for i in range(ball_count):
            speed_multiplier = random.randint(1, 6)

            velo_speed = 80 * speed_multiplier

            random_effect_1 = 1 if random.randint(1, 2) == 1 else -1
            random_effect_2 = 1 if random.randint(1, 2) == 1 else -1

            self.entities.append(
                MoveableRectangle(
                    MoveableRectangleParams(
                        group_name="velo_ball",
                        width=self.fire_ball_dimensions[0],
                        height=self.fire_ball_dimensions[1],
                        coordinates=(i * x_increment, i * y_increment),
                        color=COLOR_PRIMARY_YELLOW,
                        velocity=(
                            velo_speed * random_effect_1,
                            velo_speed * random_effect_2,
                        ),
                    )
                )
            )

    def __init__(self):
        self.create_fireballs()

        self.entities.append(
            Button(
                "Main Menu",
                lambda: scene_manager.change_scene("main_menu"),
                COLOR_PRIMARY_BLUE,
                (20, 50),
                (300, 50),
            )
        )

    def process(self, delta_time):
        fireballs = [
            entity for entity in self.entities if entity.group_name == "fireballs"
        ]

        # forces each ball positive right
        for fireball in fireballs:
            fireball.rect.x += delta_time * 100

        velo_balls = [
            entity for entity in self.entities if entity.group_name == "velo_ball"
        ]

        # TODO: add check to only reverse if it will move the rect toward center screen
        for velo_ball in velo_balls:
            # reverse velo when a ball is hit
            if (
                velo_ball.get_edge("right") > SCREEN_WIDTH
                or velo_ball.get_edge("left") < 0
            ):
                velo_ball.reverse_x_velo()
            if (
                velo_ball.get_edge("bottom") > SCREEN_HEIGHT
                or velo_ball.get_edge("top") < 0
            ):
                velo_ball.reverse_y_velo()

            velo_ball.update_pos(delta_time)


game_scene_instance = GameScene()

main_menu = Scene(
    {
        "screen": screen,
        "handle_quit": handle_quit,
        "entities": main_menu_instance.entities,
        "process": main_menu_instance.process,
        "bg_color": COLOR_PRIMARY_BLUE,
        "time_event": timer_event,
    }
)
game = Scene(
    {
        "screen": screen,
        "handle_quit": handle_quit,
        "entities": game_scene_instance.entities,
        "process": game_scene_instance.process,
        "bg_color": COLOR_PRIMARY_ORANGE,
        "time_event": timer_event,
    }
)

scene_manager.register_scene("main_menu", main_menu)
scene_manager.register_scene("game", game)

scene_manager.running = True
scene_manager.run()
