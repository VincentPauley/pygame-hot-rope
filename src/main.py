import sys

import pygame

from config import game_config
from scenes.level import Level
from scenes.main_menu import MainMenu
from scenes.rebound_experiment import RebounderExperiment

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]
FPS = 60
FONT_NAME = "Arial"

font = pygame.font.SysFont(FONT_NAME, 30)


def handle_quit():
    print("main_2.py handle quit")
    # scene_manager.running = False
    pygame.quit()
    sys.exit()


# want to figure out how to pass single function calls to scenes
# that only run one time like a close out or reset.
class Game:
    running = False

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(game_config.window.caption)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager("main_menu")

        # each scene already has access to the game state manager class
        self.main_menu = MainMenu(self.screen, self.game_state_manager)
        self.rebounder_experiment = RebounderExperiment(
            self.screen, self.game_state_manager
        )
        self.level = Level(self.screen, self.game_state_manager)

        # this dictionary stores every scene by it's key name
        self.state_map = {
            "main_menu": self.main_menu,
            "rebounder_experiment": self.rebounder_experiment,
            "level": self.level,
        }
        self.running = True

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_SPACE
                        and self.game_state_manager.get_state() == "level"
                    ):
                        self.level.receive_jump_input(delta_time)
                # don't want to iterate events more than once, instead pass spacebara click to level from here

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

            self.state_map[current_scene].run(delta_time)

            pygame.display.flip()


# game state manager is not aware of anything other than the scene name
class GameStateManager:
    task_queue = []

    def __init__(self, currentState):
        self.set_state(currentState)

    def get_state(self):
        return self.currentState

    def set_state(self, newState):
        self.currentState = newState
        self.task_queue.append({"scene_key": newState, "task": "reset"})

    def clear_task_queue(self):
        self.task_queue = []


if __name__ == "__main__":
    game = Game()
    game.run()
