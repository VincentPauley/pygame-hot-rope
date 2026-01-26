import pygame
from classes.scene import Scene, SceneConfig


class RebounderBall(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.y = 300

    def update(self):
        pass

        
class FireballRebounder(Scene):
    def __init__(self, display_screen, game_state_manager):
        super().__init__(SceneConfig(screen=display_screen))

        self.game_state_manager = game_state_manager
        self.background_image = self.asset_manager.get_image("sunset")

        # create fireball rebounder group and instantiate fireballs in that group
        self.rebounder_group = pygame.sprite.Group()
        self.rebound_ball = RebounderBall(self.asset_manager.get_image("fireball"), self.rebounder_group)

    
    def run(self, delta_time):
        self.screen.blit(self.background_image, self.background_image.get_rect())
        # self.screen.blit(self.fireball_image, self.fireball_rect)

        self.rebounder_group.draw(self.screen)

    def reset(self):
        print("class FireballRebounder: 'reset'")
        self.starting_ticks = pygame.time.get_ticks()

    def task_handler(self, task_key):
        if task_key == "reset":
            self.reset()

        self.game_state_manager.clear_task_queue()