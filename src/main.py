import pygame

from classes.scene import Scene
from config import config

pygame.init()

SCREEN_WIDTH = config["window"]["size"]["width"]
SCREEN_HEIGHT = config["window"]["size"]["height"]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(config["window"]["caption"])

main_menu = Scene({"screen": screen})
game = Scene({"screen": screen, "bg_color": (50, 50, 150)})


main_menu.activate()

# TODO: the other scenes will need to know about eachother in order to call
# eachother
