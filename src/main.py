import pygame
from pydantic import BaseModel

from config import game_config
from scene_keys import SceneKey
from scenes.level import Level
from scenes.main_menu import MainMenu
from scenes.fireball_rebounder import FireballRebounder
from scenes.rebound_experiment import RebounderExperiment

SCREEN_WIDTH = game_config.window.size["width"]
SCREEN_HEIGHT = game_config.window.size["height"]
FPS = 60
FONT_NAME = "Arial"

font = pygame.font.SysFont(FONT_NAME, 30)


class SceneConfig(BaseModel):
    key: SceneKey
    scene_class: type

    class Config:
        arbitrary_types_allowed = True


class GameParams(BaseModel):
    scenes: list[SceneConfig]

    class Config:
        arbitrary_types_allowed = True


# want to figure out how to pass single function calls to scenes
# that only run one time like a close out or reset.
class Game:
    running = False

    def __init__(self, config: GameParams):
        pygame.init()
        pygame.display.set_caption(game_config.window.caption)
        pygame.event.clear()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # set initial scene
        self.game_state_manager = GameStateManager(SceneKey.MAIN_MENU)

        # Initialize scene dictionary before registering scenes
        self.scene_dictionary = {}

        for scene in config.scenes:
            self._register_scene(scene.key, scene.scene_class)

        self.running = True

    def _handle_quit(self):
        pygame.quit()

    def _register_scene(self, scene_name, custom_class):
        self.scene_dictionary[scene_name.value] = custom_class(self.screen, self.game_state_manager)

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
                        and self.game_state_manager.get_state() == SceneKey.LEVEL.value
                    ):
                        self.scene_dictionary[SceneKey.LEVEL.value].receive_player_input("space")
            
            current_scene = self.game_state_manager.get_state()

            # find current scene's 1st task if any
            current_scene_task = next(
                (
                    t
                    for t in self.game_state_manager.task_queue
                    if t["scene_key"] == current_scene
                ),
                None,
            )

            if current_scene_task:
                print(f"processing scene: {current_scene} task: {current_scene_task['task']}")
                if current_scene_task['task'] == 'quit':
                    self._handle_quit()
                    return
                # TODO: potential here for callback that removes task from queue after completion
                self.scene_dictionary[current_scene].task_handler(current_scene_task["task"])

            # call active scene's run method at the end of every loop
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
    game = Game(GameParams(
        scenes=[
            SceneConfig(key=SceneKey.MAIN_MENU, scene_class=MainMenu),
            SceneConfig(key=SceneKey.REBOUNDER_EXPERIMENT, scene_class=RebounderExperiment),
            SceneConfig(key=SceneKey.LEVEL, scene_class=Level),
            SceneConfig(key=SceneKey.FIREBALL_REBOUNDER, scene_class=FireballRebounder)
        ]
    ))
    game.run()
