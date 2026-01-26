import pygame
from classes.scene import Scene, SceneConfig

# self.screen, self.game_state_manager

# def __init__(self, display_screen, game_state_manager):
#         super().__init__(SceneConfig(screen=display_screen))

class FireballRebounder(Scene):
    def __init__(self, display_screen, game_state_manager):
        super().__init__(SceneConfig(screen=display_screen))

        self.game_state_manager = game_state_manager
    
    def run(self, delta_time):
        self.screen.fill("red")

    def reset(self):
        print("class MainMenu: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()