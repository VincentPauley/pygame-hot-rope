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
        
        self.on_quit = scene_params["handle_quit"]

        self.entities = scene_params["entities"]

        if "bg_color" in scene_params:
            self.bg_color = scene_params["bg_color"]
        else:
            self.bg_color = (0, 0, 0)


# Short answer: you’re creating nested, blocking loops because activate() immediately runs a while loop and change_scene() calls activate() from inside that same loop. Fix by never starting a new blocking loop while another is running — either (A) drive scenes from a single central main loop, or (B) make change_scene only schedule the switch and let the current loop exit, then start the next scene.

# Recommended (A) — central main loop (preferred)

# Make Scene non-blocking: provide methods like handle_events(events), update(dt) and draw(screen) instead of _start_loop().
# SceneManager keeps current_scene and runs one main while loop that calls current_scene.handle_events/update/draw each frame. That guarantees exactly one loop.

            # ...existing code...
# def run():
#     clock = pygame.time.Clock()
#     running = True
#     current = scene_manager.scenes["main_menu"]
#     while running:
#         dt = clock.tick(60) / 1000.0
#         events = pygame.event.get()
#         for e in events:
#             if e.type == pygame.QUIT:
#                 running = False
#         current.handle_events(events)
#         current.update(dt)
#         current.draw()
#         pygame.display.flip()
# ...existing code...

    # it seems every time the active key is switched that a new while loop starts rather than fresh...
    # this seems like evidence of a bubble more than I would want.
    def _start_loop(self):
        while self.active:
            if pygame.display.get_surface() is None:
                self.active = False
                return
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                    self.on_quit()
                    return
                # note: probably want to instead just pass events down to scene controllers rather
                # than try to manage specific entity types here.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in self.entities:
                        i.detect_click(event)  # < not all entities will have this

            try:
                self.screen.fill(self.bg_color)

                for i in self.entities:
                    i.draw(self.screen)
                pygame.display.flip()
            except pygame.error as e:
                print("hitting the excecption block...")
                # common message when the window was closed: "display Surface quit"
                # stop the loop instead of letting the exception bubble up
                self.active = False
                return

    def activate(self):
        self.active = True
        self._start_loop()
