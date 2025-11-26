import math
import random
import sys

import pygame

from classes.button import Button
from classes.moveable_rectangle import MoveableRectangle, MoveableRectangleParams
from config import config

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]
FPS = 60
FONT_NAME = "Arial"

# custom colors
COLOR_PRIMARY_ORANGE = (255, 118, 35)
COLOR_PRIMARY_YELLOW = (241, 245, 72)
COLOR_PRIMARY_BLUE = (73, 114, 238)

font = pygame.font.SysFont(FONT_NAME, 30)


def handle_quit():
    print("main_2.py handle quit")
    # scene_manager.running = False
    pygame.quit()
    sys.exit()


# want to figure out how to pass single function calls to scenes
# that only run one time like a close out or reset.
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager("main_menu")

        # each scene already has access to the game state manager class
        self.main_menu = MainMenu(self.screen, self.game_state_manager)
        self.rebounder_experiment = RebounderExperiment(
            self.screen, self.game_state_manager
        )

        # this dictionary stores every scene by it's key name
        self.state_map = {
            "main_menu": self.main_menu,
            "rebounder_experiment": self.rebounder_experiment,
        }

    def run(self):
        while True:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # this checks if the game_state_manager has any scene tasks first before running the scene

            current_scene = self.game_state_manager.get_state()

            current_scene_task = next(
                (
                    t
                    for t in self.game_state_manager.task_queue
                    if t["scene_key"] == current_scene
                ),
                None,
            )
            # might want to just distribute all tasks here because what if there's closeout tasks for
            # other scenes etc?

            if current_scene_task:
                # TODO: potential here for callback that removes task from queue after completion
                self.state_map[current_scene].task_handler(current_scene_task["task"])

            self.state_map[current_scene].run(
                delta_time,
                pygame.time.get_ticks(),
            )

            pygame.display.flip()


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


# TODO: move to independent scene file
class MainMenu:
    game_ticks = 0
    active_ticks = 0
    starting_ticks = 0

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.game_state_manager = game_state_manager

        self.main_menu_buttons = define_button_group(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            "vertical",
            400,
            60,
            [
                {
                    "text": "Start Game",
                    "onclick": lambda: game_state_manager.set_state(
                        "rebounder_experiment", self.game_ticks
                    ),
                },
                {"text": "Quit", "onclick": handle_quit},
            ],
        )

    def reset(self):
        print("class MainMenu: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()
        # needs to clear task from game scene manager once completed

    # called on every frame
    # get current_scene_start out of params and into the reset function
    def run(self, delta_time, ticks):
        self.game_ticks = ticks
        self.active_ticks = ticks - self.starting_ticks
        self.screen.fill("dodgerblue")
        for button in self.main_menu_buttons:
            button.check_for_click()
            button.draw(self.screen)


# TODO: move to independent scene file
class RebounderExperiment:
    active_ticks = 0
    starting_ticks = 0
    velo_balls = []
    fire_ball_dimensions = (20, 20)

    def create_fireballs(self):
        ball_count = 25

        y_increment = SCREEN_HEIGHT / ball_count
        x_increment = SCREEN_WIDTH / ball_count

        for i in range(ball_count):
            speed_multiplier = random.randint(1, 6)

            velo_speed = 80 * speed_multiplier

            random_effect_1 = 1 if random.randint(1, 2) == 1 else -1
            random_effect_2 = 1 if random.randint(1, 2) == 1 else -1

            self.velo_balls.append(
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

    def __init__(self, display_screen, game_state_manager):
        self.screen = display_screen
        self.screen = display_screen
        self.game_state_manager = game_state_manager
        self.main_menu_button = Button(
            "Main Menu",
            lambda: game_state_manager.set_state("main_menu", pygame.time.get_ticks()),
            COLOR_PRIMARY_BLUE,
            (10, 10),
            (150, 50),
        )

        self.create_fireballs()
        self.timer_rect = pygame.Rect(SCREEN_WIDTH - (100 + 10), 10, 100, 50)

    def reset(self):
        print("class RebounderExperiment: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    # can now make specific handlers per task like reset or setup to minimize what's needed
    # inside of the run function itself :)
    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()

    # called on every frame
    def run(self, delta_time, ticks):
        self.active_ticks = ticks - self.starting_ticks

        self.screen.fill("orange")

        for velo_ball in self.velo_balls:
            if velo_ball.rect.right >= SCREEN_WIDTH and velo_ball.x_velocity > 0:
                velo_ball.reverse_x_velo()
            if velo_ball.rect.left <= 0 and velo_ball.x_velocity < 0:
                velo_ball.reverse_x_velo()
            if velo_ball.rect.bottom >= SCREEN_HEIGHT and velo_ball.y_velocity > 0:
                velo_ball.reverse_y_velo()
            if velo_ball.rect.top <= 0 and velo_ball.y_velocity < 0:
                velo_ball.reverse_y_velo()

            velo_ball.update_pos(delta_time)

        for velo_ball in self.velo_balls:
            velo_ball.draw(self.screen)

        pygame.draw.rect(self.screen, "gray24", self.timer_rect)

        timer_text_surface = font.render(
            str(math.floor(self.active_ticks / 1000)), True, "White"
        )

        # to move this out of run function would need to preset how the size and rect is treated.
        timer_text_rect = timer_text_surface.get_rect(center=self.timer_rect.center)

        self.screen.blit(timer_text_surface, timer_text_rect)

        self.main_menu_button.check_for_click()
        self.main_menu_button.draw(self.screen)


# game state manager is not aware of anything other than the scene name
class GameStateManager:
    task_queue = []

    def __init__(self, currentState):
        # self.currentState = currentState
        self.set_state(currentState, 0)
        # self.current_scene_start = 0

    def get_state(self):
        return self.currentState

    def set_state(self, newState, ticks):
        self.currentState = newState
        self.current_scene_start = ticks
        self.task_queue.append({"scene_key": newState, "task": "reset"})

    def clear_task_queue(self):
        self.task_queue = []


if __name__ == "__main__":
    game = Game()
    game.run()
