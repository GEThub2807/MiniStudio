
import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image,vitesse_x,vitesse_y):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y




