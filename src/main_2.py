import pygame

from config import config

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.game_state_manager = GameStateManager("main_menu")

        self.main_menu = MainMenu(self.screen)
        self.rebounder_experiment = RebounderExperiment(self.screen)

        # this dictionary stores every scene by it's key name
        self.state_map = {
            "main_menu": self.main_menu,
            "rebounder_experiment": self.rebounder_experiment,
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.state_map[self.game_state_manager.get_state()].run()

            pygame.display.flip()


# TODO: move to independent scene file
class MainMenu:
    def __init__(self, display_screen):
        self.screen = display_screen

    # called on every frame
    def run(self):
        self.screen.fill("dodgerblue")


# TODO: move to independent scene file
class RebounderExperiment:
    def __init__(self, display_screen):
        self.screen = display_screen

    # called on every frame
    def run(self):
        self.screen.fill("orange")


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, newState):
        self.currentState = newState


if __name__ == "__main__":
    game = Game()
    game.run()
