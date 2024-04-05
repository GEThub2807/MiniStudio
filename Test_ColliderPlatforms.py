import pygame
from pygame.locals import *


class PlateformesRythm(pygame.sprite.Sprite):

    def __init__(self, rect):
        super().__init__()
        self.rect = rect

    def afficher(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
