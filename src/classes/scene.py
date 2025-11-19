import pygame

from .button import Button


class Scene:
    """
    An independently managed game loop that controls the entire scene of the game
    for a set period of time.
    """

    active = False

    def __init__(self, scene_params):
        if scene_params["screen"] is None:
            raise ValueError("A valid pygame 'screen' param must be provided to Scene")

        self.screen = scene_params["screen"]

        if "bg_color" in scene_params:
            self.bg_color = scene_params["bg_color"]
        else:
            self.bg_color = (0, 0, 0)

        # in future the scene should register buttons dynamically
        self.start_button = Button(
            "Switch", self.switch_to_scene
        )  # need an on_click method that can call another scene

    def switch_to_scene(self):
        print("Switch to scene was called")

    def _start_loop(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_button.detect_click(event)
                    # pass event to any buttons registered in scene...

            # use provided background color or default to black
            self.screen.fill(self.bg_color)

            self.start_button.draw(self.screen)

            pygame.display.flip()

    def activate(self):
        self.active = True
        self._start_loop()
