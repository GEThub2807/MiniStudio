import pygame
from pygame.locals import *


class PlateformesRythm(pygame.sprite.Sprite):

    def __init__(self, x,y,image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image

