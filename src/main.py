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

# want to figure out how to pass single function calls to scenes
# that only run one time like a close out or reset.
class Game:
    running = False

    def __init__(self, scenes):
        pygame.init()
        pygame.display.set_caption(game_config.window.caption)
        pygame.event.clear()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager("main_menu")

        # Initialize scene dictionary before registering scenes
        self.scene_dictionary = {}

        for scene in scenes:
            self._register_scene(scene["key"], scene["class"])

        self.running = True

    def _handle_quit(self):
        pygame.quit()

    def _register_scene(self, scene_name, custom_class):
        self.scene_dictionary[scene_name] = custom_class(self.screen, self.game_state_manager)

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
                        self.scene_dictionary["level"].receive_player_input("space")
            
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
                print(f"processing scene: {current_scene} task: {current_scene_task['task']}")
                if current_scene_task['task'] == 'quit':
                    self._handle_quit()
                    return
                # TODO: potential here for callback that removes task from queue after completion
                self.scene_dictionary[current_scene].task_handler(current_scene_task["task"])

            self.scene_dictionary[current_scene].run(delta_time)

            pygame.display.flip()


# game state manager is not aware of anything other than the scene name
class GameStateManager:
    task_queue = []

    def __init__(self, currentState):
        self.set_state(currentState)

    def get_state(self):
        return self.currentState
    
    def append_task(self, scene, task):
        self.task_queue.append({"scene_key": scene, "task": task})

    def set_state(self, newState):
        self.currentState = newState
        self.task_queue.append({"scene_key": newState, "task": "reset"})

    def clear_task_queue(self):
        self.task_queue = []


if __name__ == "__main__":
    game = Game([
        {"key": "main_menu", "class": MainMenu},
        {"key": "rebounder_experiment", "class": RebounderExperiment},
        {"key": "level", "class": Level},
    ])
    game.run()
