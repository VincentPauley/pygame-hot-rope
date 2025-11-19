import pygame


class Scene:
    """
    An independently managed game loop that controls the entire scene of the game
    for a set period of time.
    """

    active = False

    def __init__(self, screen):
        self.screen = screen

    def start_loop(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                    pygame.quit()
                    return

            self.screen.fill((200, 190, 60))

            pygame.display.flip()
