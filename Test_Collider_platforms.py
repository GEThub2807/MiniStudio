import pygame
import sys

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
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.player = Player(self.player_x, self.player_y, self.image, self.vitesse_x, self.vitesse_y)
        self.player_collider = self.image.get_rect(bottomleft=(self.player.y, self.player.x))
        self.background = pygame.image.load("Assets/Fond_Game.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1400, 800))
        self.plateforme_groupe = pygame.sprite.Group()
        self.plateforme_list_rect = [pygame.Rect(0, 300, 300, 50), pygame.Rect(800, 300, 300, 50)]
        self.resistance = [0, 0]

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

            self.player_collider = self.image.get_rect(bottomleft=(self.player.y, self.player.x))
            for rectangle in self.plateforme_list_rect:
                plateforme = PlateformesRythm(rectangle)
                self.plateforme_groupe.add(plateforme)

            self.deplacer_personnage(GRAVITE)
            self.ecran.blit(self.background, (0, 0))
            self.ecran.blit(self.player.image, (self.player.x, self.player.y))

            print(self.player_collider.midbottom)
            pygame.display.flip()
            clock.tick(60)


# Lance l'instance de jeu
if __name__ == '__main__':
    pygame.init()
    Jeu().Boucle_Principale()
    pygame.quit()
