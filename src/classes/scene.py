import pygame

# needs

"""
Ok the button is being hard-coded within the init block of the function. Instead
I want to pass a class "Entity" that for now must have draw function. Entity of
a scene is an array and the scene is repsonsible for 
"""


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

        self.entities = scene_params["entities"]

        if "bg_color" in scene_params:
            self.bg_color = scene_params["bg_color"]
        else:
            self.bg_color = (0, 0, 0)

    def _start_loop(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                    pygame.quit()
                    return
                # note: probably want to instead just pass events down to scene controllers rather
                # than try to manage specific entity types here.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in self.entities:
                        i.detect_click(event)  # < not all entities will have this

            self.screen.fill(self.bg_color)

            for i in self.entities:
                i.draw(self.screen)

            pygame.display.flip()

    def activate(self):
        self.active = True
        self._start_loop()
