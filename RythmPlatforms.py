import pygame
import sys

from pygame.locals import *
from player import Player
from plateformes import PlateformesRythm


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption('Jeu of The Year')
        self.Game_Running = True
        self.Nb_Sauts = 0
        self.player_x, self.player_y = 100, 400
        self.vitesse_x, self.vitesse_y = 0, 0
        self.image = pygame.image.load('Assets/rat.png')
        self.player = Player(self.player_x, self.player_y,50,50, pygame.transform.scale(self.image, (50, 50)), self.vitesse_x,
                             self.vitesse_y)
        self.background = pygame.image.load("Assets/Fond_Game.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1400, 800))
        self.plateformes_image = pygame.image.load("Assets/Plateformes.png").convert()
        self.plateformes_image = pygame.transform.scale(self.plateformes_image, (50, 50))

        self.plateformes_list = [PlateformesRythm(100, 600, self.plateformes_image),
                                 PlateformesRythm(200, 600, self.plateformes_image),
                                 PlateformesRythm(300, 600, self.plateformes_image),
                                 PlateformesRythm(400, 600, self.plateformes_image),
                                 PlateformesRythm(500, 600, self.plateformes_image)
                                 ]

    def Afficher_Plateformes_paires(self):
        for i in range(0, len(self.plateformes_list)):
            if i % 2 == 0:
                self.ecran.blit(self.plateformes_list[i].image,
                                (self.plateformes_list[i].x, self.plateformes_list[i].y))
            else:
                self.ecran.blit(self.plateformes_list[i].image,
                                (self.plateformes_list[i].x, self.plateformes_list[i].y + 1000))

    def Afficher_Plateformes_Impaires(self):
        for j in range(0, len(self.plateformes_list)):
            if j % 2 == 0:
                self.ecran.blit(self.plateformes_list[j].image,
                                (self.plateformes_list[j].x, self.plateformes_list[j].y + 1000))
            else:
                self.ecran.blit(self.plateformes_list[j].image,
                                (self.plateformes_list[j].x, self.plateformes_list[j].y))

    def deplacer_personnage(self, gravity):

        # Appliquer la gravité au personnage
        self.player.vitesse_y += gravity

        # Mettre à jour la position du personnage
        self.player.y += self.player.vitesse_y
        self.player.x += self.player.vitesse_x

        # Limiter la position du personnage à l'écran
        self.player.x = max(0, min(self.player.x, 1400 - 50))
        self.player.y = max(0, min(self.player.y, 800 - 50))

        # Réinitialiser le nombre de sauts si le personnage touche le sol
        if self.player.y >= 800 - 50:
            self.Nb_Sauts = 0

    # Déf la boucle principale
    def Boucle_Principale(self):
        GRAVITE = 0.5
        VITESSE_X = 10
        VITESSE_Y = 10
        VITESSE_COURSE = 10
        Timer = 0
        Loop = 1
        pygame.time.set_timer(USEREVENT, 1000)

        is_running = False
        clock = pygame.time.Clock()
        while self.Game_Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.vitesse_x = -VITESSE_X
                    elif event.key == pygame.K_RIGHT:
                        self.player.vitesse_x = VITESSE_X
                    elif event.key == pygame.K_SPACE and self.Nb_Sauts < 2:
                        self.player.vitesse_y = -VITESSE_Y
                        self.Nb_Sauts += 1
                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        if not is_running:
                            VITESSE_X = VITESSE_COURSE
                            is_running = True  # La touche Shift est enfoncée
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.player.vitesse_x < 0:
                        self.player.vitesse_x = 0
                    elif event.key == pygame.K_RIGHT and self.player.vitesse_x > 0:
                        self.player.vitesse_x = 0
                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        if is_running:
                            VITESSE_X = 5
                            is_running = False  # La touche Shift est relâchée
                elif event.type == USEREVENT:
                    Timer += 1

                    if Timer == 3:
                        Loop += 1
                        Timer = 0

            self.deplacer_personnage(GRAVITE)
            self.ecran.blit(self.background, (0, 0))

            self.ecran.blit(self.player.image, (self.player.x, self.player.y))


            if Loop % 2 == 0:
                self.Afficher_Plateformes_paires()
            else:
                self.Afficher_Plateformes_Impaires()
            clock.tick(60)
            pygame.display.flip()

            print(Timer)


# Lance l'instance de jeu
if __name__ == '__main__':
    pygame.init()
    Jeu().Boucle_Principale()
    pygame.quit()
