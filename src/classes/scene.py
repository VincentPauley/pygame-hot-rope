import pygame


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

        if scene_params["entities"] is None:
            raise ValueError("A scene must provide entities in order to be valid")

        self.on_quit = scene_params["handle_quit"]

        self.entities = scene_params["entities"]

        if "bg_color" in scene_params:
            self.bg_color = scene_params["bg_color"]
        else:
            self.bg_color = (0, 0, 0)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.entities:
                    i.detect_click(event)
            if event.type == pygame.QUIT:
                self.on_quit()

    def draw(self):
        self.screen.fill(self.bg_color)
        for i in self.entities:
            i.draw(self.screen)
        pygame.display.flip()
